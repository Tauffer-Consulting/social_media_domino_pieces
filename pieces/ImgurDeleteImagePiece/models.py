from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """
    ImgurDeleteImagePiece input model
    """
    image_id: str = Field(
        default=None,
        description="The ID of the image you want to delete",
    )
    image_delete_hash: str = Field(
        description="The delete hash of the image you want to delete"
    )


class OutputModel(BaseModel):
    """
    ImgurDeleteImagePiece output model
    """
    deletion_status: int = Field(
        default=None,
        description="The status of the deletion",
    )

class SecretsModel(BaseModel): 
    """
    ImgurDeleteImagePiece secrets model
    """   
    ACCESS_TOKEN: str = Field(
        description="The user access token for the Imgur app"
    )