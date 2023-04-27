""" 
References:
- https://developers.google.com/youtube/v3/docs
- https://www.youtube.com/watch?v=D56_Cx36oGY&ab_channel=ThuVudataanalytics
"""
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import googleapiclient.discovery
import googleapiclient.errors
import os


class YoutubeListVideosPiece(BasePiece):

    def piece_function(self, input_model: InputModel):
        # Get credentials and create API client
        api_key = os.environ.get("YOUTUBE_API_KEY", None)
        client = googleapiclient.discovery.build(
            serviceName="youtube",
            version="v3",
            developerKey=api_key
        )

        # Request the list of videos from channel
        all_videos_ids = []
        while True:
            request = client.search().list(
                # part="snippet,id",
                part="id",
                type="video",
                channelId=input_model.channel_id,
                # publishedAfter="2022-12-01T00:00:00Z",  TODO: add this
                # publishedBefore=,                       TODO: add this
                maxResults=50,
            )
            response = request.execute()
            new_ids = [i["id"]["videoId"] for i in response["items"]]
            all_videos_ids.extend(new_ids)

            if "nextPageToken" not in response:
                break
        
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
                "dislikeCount": i["statistics"]["dislikeCount"],
                "commentCount": i["statistics"]["commentCount"],
            })

        msg = "Videos listing performed successfully!"
        self.logger.info(msg)

        output = OutputModel(
            message=msg,
            videos_list=all_videos,
        )

        return output