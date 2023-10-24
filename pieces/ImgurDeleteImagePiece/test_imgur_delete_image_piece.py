from domino.testing import piece_dry_run
from dotenv import load_dotenv
import os

def run_piece(
        image_delete_hash: str
):
    
    load_dotenv()
    ACCESS_TOKEN = os.environ.get("ACESS_TOKEN")

    return piece_dry_run(
        #name of the piece
        piece_name="ImgurDeleteImagePiece",

        #values to the InputModel arguments
        input_data={
            "image_delete_hash": image_delete_hash
        },
        
        #values to the SecretModel arguments
        secrets_data={ 
            "ACESS_TOKEN": ACCESS_TOKEN,
        }
    )

def test_imgur_delete_image_piece():
    output = run_piece(
        image_delete_hash=""
    )

    assert output.deletion_status == 200
