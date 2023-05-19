from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """
    InstagramPostImagePiece input model
    """
    image_url: str = Field(
        ...,
        description="public URL of the image"
    )
    caption_header: str = Field(
        default=None,
        description="optional header of the caption"
    )
    caption: str = Field(
        default = None,
        description="post caption"
    )
    caption_footer: str = Field(
        default=None,
        description="optional footer of the caption"
    )
    facebook_page_name: str = Field(
        ...,
        description = "Facebook page connected to the Instagram account"
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
        default=None,
        description="post ID"
    )


class SecretsModel(BaseModel):
    """
    InstagramPostImagePiece secrets model
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