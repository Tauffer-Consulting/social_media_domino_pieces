from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class OutputTypeType(str, Enum):
    python_list = "python_list"
    string = "string"
    json_string = "json_string"


class InputModel(BaseModel):
    """
    Get Instagram Media Input
    """
    facebook_page_name: str = Field(
        ...,
        description = "Facebook page connected to the Instagram account"
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description="output type"
    )
    id_field: bool = Field(
        default=True,
        description="if true, the id field will be returned"
    )
    media_type_field: bool = Field(
        default=True,
        description="if true, the media_type field will be returned"
    )
    caption_field: bool = Field(
        default=True,
        description="if true, the caption field will be returned"
    )
    like_count_field: bool = Field(
        default=True,
        description="if true, the like_count field will be returned"
    )
    comments_count_field: bool = Field(
        default=True,
        description="if true, the comments_count field will be returned"
    )
    permalink_field: bool = Field(
        default=True,
        description="if true, the permalink field will be returned"
    )
    timestamp_field: bool = Field(
        default=True,
        description="if true, the timestamp field will be returned"
    )
    comments_field: bool = Field(
        default=True,
        description="if true, the comments field will be returned"
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