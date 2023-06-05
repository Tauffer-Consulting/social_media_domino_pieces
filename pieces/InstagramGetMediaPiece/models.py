from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class OutputTypeType(str, Enum):
    python_list = "python_list"
    string = "string"
    json_string = "json_string"


class InstagramMediaFields(Enum):
    """
    Enum for Instagram Media Fields
    """
    media_id = "id" 
    media_type = "media_type"
    caption =  "caption"
    like_count = "like_count"
    comments_count = "comments_count"
    permalink = "permalink"
    timestamp = "timestamp"
    comments = "comments"

class InputModel(BaseModel):
    """
    Get Instagram Media Input
    """
    facebook_page_name: str = Field(
        ...,
        description = "Facebook page connected to the Instagram account"
    )
    instagram_media_fields: List[InstagramMediaFields] = Field(
        default=[InstagramMediaFields.media_id, InstagramMediaFields.media_type, InstagramMediaFields.caption, InstagramMediaFields.like_count, InstagramMediaFields.comments_count, InstagramMediaFields.permalink, InstagramMediaFields.timestamp, InstagramMediaFields.comments],
        description="list of Instagram media fields"
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description="output type"
    )

class OutputModel(BaseModel):
    """
    Get Instagram Media Output
    """
    media_list: list = Field(
        default=None,
        description="list of Instagram media posts"
    )
    media_string: str = Field(
        default=None,
        description="string of Instagram media posts"
    )
    media_json_string: str = Field(
        default=None,
        description="json string of Instagram media posts"
    )


class SecretsModel(BaseModel):
    """
    Get Instagram Media Secrets
    """
    APP_ID: str = Field(
        ...,
        description = "ID from a Facebook App"
    )
    APP_SECRET: str = Field(
        ...,
        description = "secret from a Facebook App"
    )
    ACCESS_TOKEN: str = Field(
        ...,
        description="access_token getted from a Facebook App"
    )