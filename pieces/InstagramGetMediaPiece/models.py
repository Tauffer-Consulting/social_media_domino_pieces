from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import date

class OutputTypeType(str, Enum):
    python_list = "python_list"
    string = "string"
    json_string = "json_string"


class FilterMediaTypes(str, Enum):
    ALL = "ALL"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    CAROUSEL_ALBUM = "CAROUSEL_ALBUM"

class OrderBy(str, Enum):
    likes = "Likes"
    comments = "Comments"
    date_descending = "Date Descending"

class InputModel(BaseModel):
    """
    Get Instagram Media Input
    """
    facebook_page_name: str = Field(
        ...,
        description = "Facebook page connected to the Instagram account",
    )
    max_items: int = Field(
        default=25,
        description="Max items to return",
    )
    filter_media_type: FilterMediaTypes = Field(
        default=FilterMediaTypes.ALL,
        description="Select the media media types to return.",
    )
    order_by: OrderBy = Field(
        default=OrderBy.date,
        description="Order response results by a field. This is a post processing step."
    )
    after_publish_date: Optional[date] = Field(
        default=None,
        description="After publish date.",
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.string,
        description="output type",
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
    INSTAGRAM_APP_ID: str = Field(
        ...,
        description = "ID from a Facebook App"
    )
    INSTAGRAM_APP_SECRET: str = Field(
        ...,
        description = "Facebook app secret"
    )
    INSTAGRAM_ACCESS_TOKEN: str = Field(
        ...,
        description="Long lived token from a Facebook App"
    )