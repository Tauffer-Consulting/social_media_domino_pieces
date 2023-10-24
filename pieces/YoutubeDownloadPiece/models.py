from pydantic import BaseModel, Field
from enum import Enum


class OutputTypeType(str, Enum):
    audio = "audio"
    video = "video"


class InputModel(BaseModel):
    """
    Input data for YoutubeDownloadPiece
    """
    url: str = Field(
        description='The url of the video to be downloaded.',
        required=True
    )
    output_type: OutputTypeType = Field(
        description='The type of output file to be downloaded.',
        default=OutputTypeType.audio,
        required=True
    )


class OutputModel(BaseModel):
    """
    Output data for YoutubeDownloadPiece
    """
    message: str = Field(
        default="",
        description="Output message to log"
    )
    file_path: str = Field(
        description="The path to the downloaded file"
    )