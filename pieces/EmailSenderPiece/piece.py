from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from email.message import EmailMessage
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

    def piece_function(self, input_model: InputModel):

        email_account = self.secrets.EMAIL_SENDER_ACCOUNT
        email_password = self.secrets.EMAIL_SENDER_PASSWORD

        email_server = servers[input_model.email_provider]

        email_receivers = [r.strip() for r in input_model.email_receivers.split(",")]

        email_subject = input_model.email_subject.format(**{arg.arg_name: arg.arg_value for arg in input_model.subject_args}) if input_model.subject_args else input_model.email_subject
        email_body = input_model.email_body.format(**{arg.arg_name: arg.arg_value for arg in input_model.body_args}) if input_model.body_args else input_model.email_body

        email_message = EmailMessage()
        email_message["From"] = email_account
        email_message["To"] = email_receivers
        email_message["Subject"] = email_subject
        email_message.set_content(email_body)

        context = ssl.create_default_context()

        self.logger.info("Sending email")
        try:
            with smtplib.SMTP_SSL(email_server, 465, context=context) as service:
                service.login(email_account, email_password)
                service.sendmail(email_account, email_receivers, email_message.as_string())
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

        return OutputModel(
            message=msg,
            success=success,
            error=error
        )