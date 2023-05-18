from domino.base_piece import BasePiece
from .models import InputModel, OutputModel

import requests
import json
from urllib.parse import quote, urljoin

class InstagramPostImagePiece(BasePiece):

    host_domain = 'https://graph.facebook.com/'
    graph_api_version = 'v15.0'
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

        response = dict()
        response['json_content'] = json.loads(data.content)
        response['json_content_pretty'] = json.dumps(json.loads(data.content), indent=2)
        response['url'] = url
        response['endpoint_query_params'] = endpoint_query_params
    
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
        url = urljoin(cls.endpoint_base_path, page_id)
        endpoint_query_params = f'access_token={access_token}&fields=instagram_business_account'

        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='get')

        return response['json_content']['instagram_business_account']['id']
    
    @classmethod
    def create_container(cls, access_token:str, instagram_business_account:str, image_url:str, caption:str):
        caption = quote(caption, safe='') #HTML URL encode for the caption parameter

        url = urljoin(cls.endpoint_base_path, f'{instagram_business_account}/media') 
        endpoint_query_params = f'image_url={image_url}&caption={caption}&access_token={access_token}'

        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='post')
        
        return response['json_content']['id']
    
    @classmethod
    def publish_container(cls, access_token:str, instagram_business_account:str, container_id:str):
        url = urljoin(cls.endpoint_base_path, f'{instagram_business_account}/media_publish')
        endpoint_query_params = f'creation_id={container_id}&access_token={access_token}'

        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='post')

        return response['json_content']['id']
    
    @classmethod
    def get_post_permalink(cls, access_token:str, post_id: str):
        url = urljoin(cls.endpoint_base_path, f'{post_id}')
        endpoint_query_params = f'fields=permalink&access_token={access_token}'
        
        response = cls.make_api_call(url=url, endpoint_query_params=endpoint_query_params, request_method='get')

        return response['json_content']['permalink']

    def piece_function(self, input_model: InputModel):
        
        app_id = self.secrets.APP_ID
        app_secret = self.secrets.APP_SECRET
        access_token = self.secrets.ACCESS_TOKEN

        long_lived_access_token = self.secrets.ACCESS_TOKEN = self.get_long_lived_access_token(app_id=app_id, app_secret=app_secret, access_token=access_token)

        self.logger.info("Getting information about the Instagram Account")
        page_id = self.get_page_id(access_token=long_lived_access_token, facebook_page_name=input_model.facebook_page_name)

        instagram_business_account = self.get_instagram_business_account(access_token=long_lived_access_token, page_id=page_id)

        caption = f"{input_model.caption_header}\n{input_model.caption}" if input_model.caption_header else input_model.caption
        caption += f"\n{input_model.caption_footer}" if input_model.caption_footer else ""

        self.logger.info("Creating the post")        
        container_id = self.create_container(access_token=long_lived_access_token, instagram_business_account=instagram_business_account, image_url=input_model.image_url, caption=caption)

        self.logger.info("Publishing the post")
        post_id = self.publish_container(access_token=long_lived_access_token, instagram_business_account=instagram_business_account, container_id=container_id)

        permalink = self.get_post_permalink(access_token=long_lived_access_token, post_id=post_id)

        self.format_display_result(input_model=input_model, permalink=permalink)

        return OutputModel(
            message="Post successfully completed!",
            post_id=post_id
        )
    
    def format_display_result(self, input_model: InputModel, permalink: str):
        md_text = f"""
## Link of the post
{permalink}

"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }