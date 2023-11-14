from pydantic import BaseModel, Field
from typing import Optional, List


class InputModel(BaseModel):
    """
    InstagramPostImagePiece input model
    """
    image_url: str = Field(
        ...,
        description="public URL of the image",
    )
    caption: str = Field(
        default="",
        description="post caption"
    )
    hashtags: List[str] = Field(
        default=[],
        description="Optional hashtags to attach to caption footer"
    )
    facebook_page_name: str = Field(
        ...,
        description = "Facebook page connected to the Instagram account",
        
    )

class OutputModel(BaseModel):
    """
    InstagramPostImagePiece output model
    """
    message: str = Field(
        default="",
        description="output message to log"
    )
    post_id: str = Field(
        description="post ID"
    )
    post_link: str = Field(
        description="post link"
    )


class SecretsModel(BaseModel):
    """
    InstagramPostImagePiece secrets model
    """
    INSTAGRAM_APP_ID: str = Field(
        ...,
        description = "ID from a Facebook App"
    )
    INSTAGRAM_APP_SECRET: str = Field(
        ...,
        description = "secret from a Facebook App"
    )
    INSTAGRAM_ACCESS_TOKEN_TEST: str = Field(
        ...,
        description="access_token getted from a Facebook App"
    )