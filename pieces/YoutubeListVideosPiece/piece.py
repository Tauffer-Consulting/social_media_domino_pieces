""" 
References:
- https://developers.google.com/youtube/v3/docs
- https://www.youtube.com/watch?v=D56_Cx36oGY&ab_channel=ThuVudataanalytics
"""
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
from dateutil import parser
from typing import List

class YoutubeListVideosPiece(BasePiece):

    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):
        # Get credentials and create API client
        api_key = secrets_data.YOUTUBE_API_KEY
        client = googleapiclient.discovery.build(
            serviceName="youtube",
            version="v3",
            developerKey=api_key
        )

        # input arguments
        channel_username = input_data.channel_username

        request = client.channels().list(
            part="id",
            forUsername=channel_username 
        )
        response = request.execute()
        channel_id = response["items"][0]["id"]


        # converting date to RFC 3339 format
        published_after = f"{datetime.isoformat(parser.parse(input_data.published_at_or_after.isoformat()))}Z" if input_data.published_at_or_after else None
        published_before = f"{datetime.isoformat(parser.parse(input_data.published_at_or_before.isoformat()))}Z" if input_data.published_at_or_before else None

        max_videos = input_data.max_videos
        order_by = input_data.order_by.value
        video_duration = input_data.video_duration.value
        next_page_token = None

        # Request the list of videos from channel
        all_videos_ids = []
        while max_videos > 0:
            max_results = min(max_videos, 50)
            max_videos -= max_results
            request = client.search().list(
                # part="snippet,id",
                part="snippet",
                type="video",
                channelId=channel_id,
                publishedAfter=published_after,
                publishedBefore=published_before,
                maxResults=max_results,
                order=order_by,
                videoDuration = video_duration,
                pageToken=next_page_token
            )
            response = request.execute()
            new_ids = [i["id"]["videoId"] for i in response["items"]]
            all_videos_ids.extend(new_ids)

            if "nextPageToken" not in response:
                break
            next_page_token = response["nextPageToken"]
        
        # Get videos details
        videos_ids_string = ",".join(all_videos_ids)
        request = client.videos().list(
            part="contentDetails,snippet,statistics",
            id=videos_ids_string,
        )
        response = request.execute()
        
        all_videos = []
        for i in response["items"]:
            all_videos.append({
                "id": i["id"],
                "url": f"https://www.youtube.com/watch?v={i['id']}", 
                "title": i["snippet"]["title"],
                "description": i["snippet"]["description"],
                "publishedAt": i["snippet"]["publishedAt"],
                "thumbnail": i["snippet"]["thumbnails"]["default"]["url"],
                "duration": i["contentDetails"]["duration"],
                "viewCount": i["statistics"]["viewCount"],
                "likeCount": i["statistics"]["likeCount"],
                "commentCount": i["statistics"]["commentCount"],
            })

        msg = "Videos listing performed successfully!"
        self.logger.info(msg)

        # Display result in the Domino GUI
        self.format_display_result(all_videos)

        return OutputModel(
            message=msg,
            videos_list=all_videos,
        )
    
    def format_display_result(self, video_list: List):
        md_text = "## List of videos:  \n\n"

        for video in video_list:
            md_text += f"**Title:** {video['title']}  \n"
            md_text += f"**Description:** {video['description']}  \n"
            md_text += f"**Published At:** {video['publishedAt']}  \n"
            md_text += f"**View Count:** {video['viewCount']}  \n"
            md_text += f"**Like Count:** {video['likeCount']}  \n"
            md_text += f"**Comment Count:** {video['commentCount']}  \n"
            md_text += f"**URL:** [{video['url']}]({video['url']})  \n"
            md_text += f"**Thumbnail:**   \n![Thumbnail]({video['thumbnail']})  \n"
            md_text += f"**Duration:** {video['duration']}  \n\n"

        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }