from domino.testing import piece_dry_run
import os
import pytest


def run_piece(
    image_delete_hash: str
):
    
    IMGUR_ACESS_TOKEN = os.environ.get("IMGUR_ACESS_TOKEN")

    return piece_dry_run(
        #name of the piece
        piece_name="ImgurDeleteImagePiece",

        #values to the InputModel arguments
        input_data={
            "image_delete_hash": image_delete_hash
        },
        
        #values to the SecretModel arguments
        secrets_data={ 
            "ACESS_TOKEN": IMGUR_ACESS_TOKEN,
        }
    )

@pytest.mark.skip(reason="")
def test_imgur_delete_image_piece():
    output = run_piece(
        image_delete_hash=""
    )

    assert output.get("deletion_status") == 200
