from pydantic import BaseModel, Field


class InputModel(BaseModel):
    """
    Input data for YoutubeListVideosPiece
    """
    channel_id: str = Field(
        description='The Id of the Youtube channel.'
    )


class OutputModel(BaseModel):
    """
    Output data for YoutubeListVideosPiece
    """
    message: str = Field(
        default="",
        description="Output message to log"
    )
    videos_list: list = Field(
        description="A list containing information about videos."
    )


class SecretsModel(BaseModel):
    """
    Secrets data for YoutubeListVideosPiece
    """
    YOUTUBE_API_KEY: str = Field(
        description="The Youtube Data API Key."
    )