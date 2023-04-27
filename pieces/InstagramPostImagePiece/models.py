from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """
    Publish an image on Intagram
    """
    image_url: str = Field(
        ...,
        description='public URL of the image'
    )
    caption: str = Field(
        default = None,
        description='post caption'
    )
    facebook_page_name: str = Field(
        ...,
        description = 'Facebook page connected to the Instagram account'
    )

class OutputModel(BaseModel):
    """
    Publish an image on Intagram
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
    Example Piece Secrets
    """
    APP_ID: str = Field(
        ...,
        description = 'ID from a Facebook App'
    )
    APP_SECRET: str = Field(
        ...,
        description = 'secret from a Facebook App'
    )
    ACCESS_TOKEN: str = Field(
        ...,
        description='access_token getted from a Facebook App'
    )