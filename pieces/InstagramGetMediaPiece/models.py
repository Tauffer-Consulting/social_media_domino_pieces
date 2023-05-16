from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """
    Get Instagram Media Input
    """
    facebook_page_name: str = Field(
        ...,
        description = "Facebook page connected to the Instagram account"
    )

class OutputModel(BaseModel):
    """
    Get Instagram Media Output
    """
    media_list: list = Field(
        description="list of Instagram media posts"
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