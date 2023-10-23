from domino.testing import piece_dry_run
from typing import List, Dict
from pydantic import FilePath

def run_piece(
    email_receivers: str, 
    email_subject: str, 
    subject_args: List[Dict] , 
    email_body: str, 
    body_args: List[Dict], 
    attachment_path: FilePath = None
):

    return piece_dry_run(
        #name of the piece
        piece_name="EmailSenderPiece",

        #values to the InputModel arguments
        input_data={
            "email_receivers": email_receivers,
            "email_subject": email_subject,
            "subject_args": subject_args,
            "email_body": email_body,
            "body_args": body_args,
            "attachment_path": attachment_path,
        },

        #values to the SecretModel arguments
        secrets_data={ 
            "EMAIL_SENDER_ACCOUNT": EMAIL_SENDER_ACCOUNT,
            "EMAIL_SENDER_PASSWORD": EMAIL_SENDER_PASSWORD,

        }

    )

def test_email_sender_piece():
    output = run_piece(
        email_receivers="",
        email_subject="Email test with attachment. Testing subject arg: {argument}",
        subject_args=[{"arg_name": "argument", "arg_value": "Arg subject value", "arg_type": "string"}],
        email_body="This is a body of an email. Testing body arg: {argument}",
        body_args=[{"arg_name": "argument", "arg_value": "Arg body value", "arg_type": "string"}],
    )
    
    assert output.message == "Email sent successfully."
    assert output.success == True
    assert output.error == ""
