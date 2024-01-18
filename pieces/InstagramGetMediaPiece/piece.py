from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel, FilterMediaTypes, OrderBy
from typing import List, Optional
from datetime import date, datetime, time as dt_time
import requests
import json

class InstagramGetMediaPiece(BasePiece):

    host_domain = 'https://graph.facebook.com/'
    graph_api_version = 'v18.0'
    endpoint_base_path = f'{host_domain}{graph_api_version}/'

    @staticmethod
    def make_api_call(url:str, endpoint_query_params:str, request_method='get'):
        if request_method == 'get':
            try:
                data = requests.get(url=url, params=endpoint_query_params)
            except Exception as e:
                print(e)
        elif request_method == 'post':
            try:
                data = requests.post(url=url, params=endpoint_query_params)
            except Exception as e:
                print(e)
        else:
            raise ValueError('request_method must be: "get" or "post"')

        response = {}
        response['url'] = url
        response['endpoint_query_params'] = endpoint_query_params
        response['json_content'] = json.loads(data.content)

        return response

    @classmethod
    def get_long_lived_access_token(cls, app_id:str, app_secret:str, access_token:str):
        url = cls.endpoint_base_path + 'oauth/access_token'
        endpoint_query_params = f'grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={access_token}'
        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='get')
        return response['json_content']['access_token']

    @classmethod
    def get_page_id(cls, access_token:str, facebook_page_name:str):
        url = cls.endpoint_base_path + 'me/accounts'
        endpoint_query_params = f'access_token={access_token}'

        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='get')

        for i in response['json_content']['data']:
            if i['name'] == facebook_page_name:
                return i['id']

        raise Exception(f'Page "{facebook_page_name}" not found')

    @classmethod
    def get_instagram_business_account(cls, access_token:str, page_id:str):
        url = f'{cls.endpoint_base_path}{page_id}'
        endpoint_query_params = f'access_token={access_token}&fields=instagram_business_account'

        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='get')

        return response['json_content']['instagram_business_account']['id']

    @classmethod
    def get_media_list(
        cls,
        access_token: str,
        instagram_business_account: str,
        media_fields: List,
        max_items: int,
        since_timestamp: Optional[int] = None,
        filter_media_type: FilterMediaTypes = FilterMediaTypes.ALL
    ):
        url = f'{cls.endpoint_base_path}{instagram_business_account}/media'
        str_fields = ','.join(media_fields)
        endpoint_query_params = f'access_token={access_token}&fields={str_fields}&limit={max_items}'

        if since_timestamp:
            endpoint_query_params += f'&since={since_timestamp}'

        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='get')

        if filter_media_type == FilterMediaTypes.ALL:
            output_data = response['json_content']['data']
        else:
            output_data = [i for i in response['json_content']['data'] if i['media_type'] == filter_media_type.value]

        while response['json_content'].get('paging').get('next') and len(output_data) < max_items:
            response = cls.make_api_call(url=response['json_content']['paging']['next'], endpoint_query_params='', request_method='get')

            if filter_media_type != FilterMediaTypes.ALL:
                output_data += [i for i in response['json_content']['data'] if i['media_type'] == filter_media_type.value]
                continue

            output_data += response['json_content']['data']

        return output_data

    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):
        app_id = secrets_data.INSTAGRAM_APP_ID
        app_secret = secrets_data.INSTAGRAM_APP_SECRET
        access_token = secrets_data.INSTAGRAM_ACCESS_TOKEN

        # Force API to return media_type
        user_selected_media_type_field = input_data.media_type_field
        filter_media_type = input_data.filter_media_type
        if filter_media_type != "ALL":
            input_data.media_type_field = True



        fields = {
            "id_field": "id",
            "media_type_field":"media_type",
            "caption_field": "caption",
            "like_count_field": "like_count",
            "comments_count_field": "comments_count",
            "permalink_field": "permalink",
            "timestamp_field": "timestamp",
            "comments_field": "comments"
        }

        inputs = json.loads(input_data.model_dump_json())
        selected_fields = [fields.get(key) for key, value in inputs.items() if value == True]

        if input_data.order_by.value != OrderBy.date_descending.value:
            if not inputs.get(input_data.order_by.name):
                raise ValueError(f"Field {input_data.order_by.name} must be selected to order by it")

        long_lived_access_token = secrets_data.INSTAGRAM_ACCESS_TOKEN = self.get_long_lived_access_token(app_id=app_id, app_secret=app_secret, access_token=access_token)
        page_id = self.get_page_id(access_token=long_lived_access_token, facebook_page_name=input_data.facebook_page_name)
        instagram_business_account = self.get_instagram_business_account(access_token=long_lived_access_token, page_id=page_id)

        since_timestamp = None
        if input_data.after_publish_date:
            datetime_publish_date = datetime.combine(input_data.after_publish_date, dt_time(0, 0, 0))
            since_timestamp = int(datetime_publish_date.timestamp())

        media_list = self.get_media_list(
            access_token=long_lived_access_token,
            instagram_business_account=instagram_business_account,
            media_fields=selected_fields,
            max_items=input_data.max_items,
            since_timestamp=since_timestamp,
            filter_media_type=filter_media_type
        )

        selected_media_fields = []
        for media in media_list:
            selected_media = {}
            for field, value in media.items():
                if (field == 'media_type' and not user_selected_media_type_field) or field not in selected_fields:
                    continue
                selected_media[field] = value
            selected_media_fields.append(selected_media)

        # Order results by like_count
        if input_data.order_by.value == OrderBy.like_count.value:
            selected_media_fields = sorted(selected_media_fields, key=lambda x: x['like_count'], reverse=True)
        elif input_data.order_by.value == OrderBy.comments.value:
            selected_media_fields = sorted(selected_media_fields, key=lambda x: len(x.get('comments', {}).get('data', [])), reverse=True)
        elif input_data.order_by.value == OrderBy.date.value:
            selected_media_fields = sorted(selected_media_fields, key=lambda x: x['timestamp'], reverse=True)


        #selected_media_fields = [dict((field, value) for field, value in media.items() if field in selected_fields) for media in media_list]

        # Display result in the Domino GUI
        self.format_display_result(input_data, selected_media_fields)

        if input_data.output_type == "string":
            media_string = ""
            for i in selected_media_fields:
                media_string += '  \n'.join([f"{key}: {str(value)}" for key, value in i.items()])
                media_string += '  \n\n'
            return OutputModel(
                media_string=media_string
            )

        if input_data.output_type == "python_list":
            python_list = []
            for i in media_list:
                python_list.append(dict((key, value) for key, value in i.items() if key in selected_fields))
            return OutputModel(
                media_list=python_list
            )

        if input_data.output_type == "json_string":
            json_string = "\n".join(json.dumps(i, indent=4) for i in selected_media_fields)
            return OutputModel(
                media_json_string=json_string
            )

    def format_display_result(self, input_data: InputModel, media_list: List):
        # json_media_list = '\n\n'.join(json.dumps(i, indent=4) for i in media_list)
        md_text = f"""
## Media list:

"""
        for media in media_list:
            for key, value in media.items():
                md_text += f"- **{key}:** {str(value)}  \n"
        md_text += f"## Args  \n**facebook page name**: {input_data.facebook_page_name}"

        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
