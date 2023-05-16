from pydantic import BaseModel, Field

class InputModel(BaseModel):
    """
    Imgur Uploader Piece Input
    """
    image_path: str = Field(
        description="The path to your local image",
    )

class OutputModel(BaseModel):
    """
    Imgur Uploader Piece Output
    """
    image_url: str = Field(
        description="The URL to your uploaded image",
    )

class SecretsModel(BaseModel): 
    """
    Imgur Uploader Piece Secrets
    """   
    CLIENT_ID: str = Field(
        description="The app client ID"
    )

    CLIENT_SECRET: str = Field(
        description="The app client secret"
    )