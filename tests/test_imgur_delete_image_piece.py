from domino.scripts.piece_dry_run import piece_dry_run
from dotenv import load_dotenv
import os

def run_piece(
        image_delete_hash: str
):
    
    load_dotenv()
    ACCESS_TOKEN = os.environ.get("ACESS_TOKEN")

    return piece_dry_run(
        #local piece repository path
        repository_folder_path="../",

        #name of the piece
        piece_name="ImgurDeleteImagePiece",

        #values to the InputModel arguments
        piece_input={
            "image_delete_hash": image_delete_hash
        },
        
        #values to the SecretModel arguments
        secrets_input={ 
            "ACESS_TOKEN": ACCESS_TOKEN,
        }
    )

def test_piece():
    output = run_piece(
        image_delete_hash=""
    )

    assert output.deletion_status == 200

if __name__ == "__main__":
    test_piece()
