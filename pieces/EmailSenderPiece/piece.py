from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union
import ssl
import smtplib
import os


servers = {
    "gmail": "smtp.gmail.com",
    "outlook": "smtp-mail.outlook.com",
    "office365": "smtp.office365.com",
    "yahoo": "smtp.mail.yahoo.com",
}

class EmailSenderPiece(BasePiece):

    def create_attachment(self, attachment_path: str = None):
        if not os.path.exists(attachment_path):
            raise FileNotFoundError(f"Attachment path {attachment_path} does not exist")
        with open(attachment_path, "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition",f"attachment; filename={os.path.basename(attachment_path)}",)
        return attachment

    def piece_function(self, input_model: InputModel):

        email_account = self.secrets.EMAIL_SENDER_ACCOUNT
        email_password = self.secrets.EMAIL_SENDER_PASSWORD

        email_server = servers[input_model.email_provider]

        list_email_receivers = [r.strip() for r in input_model.email_receivers.split(",")]
        str_email_receivers = input_model.email_receivers

        email_subject = input_model.email_subject.format(**{arg.arg_name: arg.arg_value for arg in input_model.subject_args}) if input_model.subject_args else input_model.email_subject
        email_body = input_model.email_body.format(**{arg.arg_name: arg.arg_value for arg in input_model.body_args}) if input_model.body_args else input_model.email_body

        email_attachment = input_model.attachment_path

        email_message = MIMEMultipart()
        email_message["From"] = email_account
        email_message["To"] = str_email_receivers
        email_message["Subject"] = email_subject
        email_message.attach(MIMEText(email_body, "plain"))


        if email_attachment:
            attachment = self.create_attachment(email_attachment)
            email_message.attach(attachment)

        context = ssl.create_default_context()        
        self.logger.info("Sending email")
        try:
            with smtplib.SMTP_SSL(email_server, 465, context=context) as service:
                service.login(email_account, email_password)
                service.sendmail(email_account, list_email_receivers, email_message.as_string())
            msg = "Email sent successfully."
            self.logger.info(msg)
            success = True
            error = ""
        except Exception as e:
            msg = "Error sending email."
            self.logger.info(msg)
            success = False
            error = str(e)
            print(error)
            raise e
        
        self.format_display_result(email_account, str_email_receivers, email_subject, email_body, email_attachment)

        return OutputModel(
            message=msg,
            success=success,
            error=error
        )
    
    def format_display_result(self, email_account: str, str_email_receivers: str, email_subject: str, email_body: str, email_attachment_path: Union[str, None]):
        md_text = f"""
## Email Sender:  \n
{email_account}  \n
## Email Receivers:  \n 
{str_email_receivers}  \n
## Email Subject:  \n
{email_subject}  \n
## Email Body:  \n
{email_body}  \n 
"""
        if  email_attachment_path:
            md_text += f"""## Email Attachment File Name:  \n{os.path.basename(email_attachment_path)}  \n"""

        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }