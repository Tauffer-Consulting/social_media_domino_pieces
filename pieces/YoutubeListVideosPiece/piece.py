""" 
References:
- https://developers.google.com/youtube/v3/docs
- https://www.youtube.com/watch?v=D56_Cx36oGY&ab_channel=ThuVudataanalytics
"""
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
from dateutil import parser


class YoutubeListVideosPiece(BasePiece):

    def piece_function(self, input_model: InputModel):
        # Get credentials and create API client
        api_key = self.secrets.YOUTUBE_API_KEY
        client = googleapiclient.discovery.build(
            serviceName="youtube",
            version="v3",
            developerKey=api_key
        )

        # input arguments
        channel_id = input_model.channel_id

        # converting date to RFC 3339 format
        published_after = f"{datetime.isoformat(parser.parse(input_model.published_at_or_after.isoformat()))}Z" if input_model.published_at_or_after else None
        published_before = f"{datetime.isoformat(parser.parse(input_model.published_at_or_before.isoformat()))}Z" if input_model.published_at_or_before else None

        max_videos = input_model.max_videos
        order_by = input_model.order_by.value
        video_duration = input_model.video_duration.value
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

        output = OutputModel(
            message=msg,
            videos_list=all_videos,
        )

        return output