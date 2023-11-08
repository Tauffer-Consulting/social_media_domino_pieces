from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Union


class ProviderType(str, Enum):
    gmail = "gmail"
    outlook = "outlook"
    office365 = "office365"
    yahoo = "yahoo"


class InnerArgModel(BaseModel):
    """
    Inner argument model to use in the body and subject texts
    """
    arg_name: str
    arg_value: Union[str, int, float, bool]


class InputModel(BaseModel):
    """
    Input data for EmailSenderPiece
    """
    email_provider: ProviderType = Field(
        description='The email provider to use',
        default=ProviderType.gmail,
    )
    email_receivers: str = Field(
        description='The receivers of the email, as comma-separated values',
    )
    email_subject: str = Field(
        description='The subject of the email.',  
    )
    subject_args: Optional[List[InnerArgModel]] = Field(
        default=None,
        description="List of arguments to insert into the subject of the email",
    )
    email_body: str = Field(
        description='The body of the email.',
    )
    body_args: Optional[List[InnerArgModel]] = Field(
        default=None,
        description="List of arguments to insert into the body of the email",
    )
    attachment_path: Optional[str] = Field(
        default=None,
        description="Path to the attachment file"
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
