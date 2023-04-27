from pydantic import BaseModel, Field
from enum import Enum


class ProviderType(str, Enum):
    gmail = "gmail"
    outlook = "outlook"
    office365 = "office365"
    yahoo = "yahoo"


class InputModel(BaseModel):
    """
    Input data for EmailSenderPiece
    """
    email_provider: ProviderType = Field(
        description='The email provider to use.',
        default=ProviderType.gmail
    )
    email_receivers: str = Field(
        description='The receivers of the email, as comma-separated values.'
    )
    email_subject: str = Field(
        description='The subject of the email.'
    )
    email_body: str = Field(
        description='The body of the email.'
    )


class OutputModel(BaseModel):
    """
    Output data for EmailSenderPiece
    """
    message: str = Field(
        default="",
        description="Output message to log."
    )
    success: bool = Field(
        description="The result of the email sending task."
    )
    error: str = Field(
        default="",
        description="The error message, if any."
    )


class SecretsModel(BaseModel):
    """
    Secrets data for EmailSenderPiece
    """
    EMAIL_SENDER_ACCOUNT: str = Field(
        description="The email sender account."
    )
    EMAIL_SENDER_PASSWORD: str = Field(
        description="The email sender password"
    )