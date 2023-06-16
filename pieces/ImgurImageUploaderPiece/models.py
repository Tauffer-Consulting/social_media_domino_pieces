from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """
    ImgurImageUploaderPiece input model
    """
    image_path: str = Field(
        description="The path to your local image",
    )


class OutputModel(BaseModel):
    """
    ImgurImageUploaderPiece output model
    """
    image_url: str = Field(
        description="The URL to your uploaded image",
    )
    image_delete_hash: str = Field(
        description="The delete hash for your uploaded image",
    )


class SecretsModel(BaseModel): 
    """
    ImgurImageUploaderPiece secrets model
    """   
    CLIENT_ID: str = Field(
        description="The app client ID"
    )

    CLIENT_SECRET: str = Field(
        description="The app client secret"
    )