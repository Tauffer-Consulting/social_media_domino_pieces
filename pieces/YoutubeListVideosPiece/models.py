from pydantic import BaseModel, Field
from enum import Enum
from datetime import date

class OrderBy(str, Enum):
    """
    The order in which the videos are returned.
    """
    date = "date"
    rating = "rating"
    relevance = "relevance"
    title = "title"
    video_count = "videoCount"
    view_count = "viewCount"

class VideoDuration(str, Enum):
    """
    The duration of the video.
    """
    any = "any" 
    # Only include videos longer than 20 minutes
    long = "long" 
    # Only include videos that are between 4 and 20 minutes long (inclusive)
    medium = "medium"
    # Only include videos that are less than four minutes long
    short = "short"

class InputModel(BaseModel):
    """
    Input data for YoutubeListVideosPiece
    """
    channel_id: str = Field(
        description='The Id of the Youtube channel.'
    )
    max_videos: int = Field(
        default=10,
        description='The maximum number of videos to be returned',
        gt=0
    )
    published_at_or_after: date = Field(
        default=None,
        description='Filter videos created at or after the specified date'
    )
    published_at_or_before: date = Field(
        default=None,
        description='Filter videos created before or at the specified date'
    )
    order_by: OrderBy = Field(
        default=OrderBy.date,
        description='The order in which the videos are returned'
    )
    video_duration: VideoDuration = Field(
        default=VideoDuration.any,
        description='The duration of the video'
    )


class OutputModel(BaseModel):
    """
    Output data for YoutubeListVideosPiece
    """
    message: str = Field(
        default="",
        description="Output message to log"
    )
    videos_list: list = Field(
        description="A list containing information about videos."
    )


class SecretsModel(BaseModel):
    """
    Secrets data for YoutubeListVideosPiece
    """
    YOUTUBE_API_KEY: str = Field(
        default=None,
        description="The Youtube Data API Key."
    )