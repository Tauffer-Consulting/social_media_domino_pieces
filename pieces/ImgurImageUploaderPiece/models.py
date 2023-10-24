from pydantic import BaseModel, Field
from typing import Optional


class InputModel(BaseModel):
    """
    ImgurImageUploaderPiece input model
    """
    image_path: str = Field(
        description="The path to your local image",
    )
    image_title: Optional[str] = Field(
        default=None,
        description="The title for your image",
    )
    image_description: Optional[str] = Field(
        default=None,
        description="The description for your image",
    )
    id_as_output: bool = Field(
        default=True,
        description="If true, the image id will be returned as an output",
    )
    title_as_output: bool = Field(
        default=True,
        description="If true, the image title will be returned as an output",
    )
    description_as_output: bool = Field(
        default=True,
        description="If true, the image description will be returned as an output",
    )
    delete_hash_as_output: bool = Field(
        default=True,
        description="If true, the image delete hash will be returned as an output",
    )
    url_as_output: bool = Field(
        default=True,
        description="If true, the image link will be returned as an output",
    )


class OutputModel(BaseModel):
    """
    ImgurImageUploaderPiece output model
    """
    image_id: str = Field(
        default=None,
        description="The image id",
    )
    image_title: str = Field(
        default=None,
        description="The image title",
    )
    image_description: str = Field(
        default=None,
        description="The image description",
    )
    image_delete_hash: str = Field(
        description="The delete hash for your uploaded image",
    )
    image_url: str = Field(
        default=None,
        description="The URL to your uploaded image",
    )


class SecretsModel(BaseModel): 
    """
    ImgurImageUploaderPiece secrets model
    """   
    CLIENT_ID: str = Field(
        description="The Imgur app client ID"
    )