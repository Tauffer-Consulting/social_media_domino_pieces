from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import date

class OrderBy(str, Enum):
    """
    The order in which the videos are returned.
    """
    date = "date"
    rating = "rating"
    relevance = "relevance"
    title = "title"
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
    channel_username: str = Field(
        default=None,
        description='The username of the Youtube channel.',
    )
    max_videos: int = Field(
        default=10,
        description='The maximum number of videos to be returned',
        gt=0,

    )
    published_at_or_after: Optional[date] = Field(
        default=None,
        description='Filter videos created at or after the specified date'
    )
    published_at_or_before: Optional[date] = Field(
        default=None,
        description='Filter videos created before or at the specified date'
    )
    order_by: OrderBy = Field(
        default=OrderBy.date,
        description='The order in which the videos are returned',
        title="Order By",

    )
    video_duration: VideoDuration = Field(
        default=VideoDuration.any,
        description='The duration of the video',
        title="Video Duration",
    )
    return_only_urls: bool = Field(
        default=False,
        description='If True, only the urls of the videos will be returned',
        title="Return only urls"
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
        description="The Youtube Data API Key."
    )
