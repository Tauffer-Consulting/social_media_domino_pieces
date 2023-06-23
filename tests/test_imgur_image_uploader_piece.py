from domino.scripts.piece_dry_run import piece_dry_run
from dotenv import load_dotenv
from pydantic import FilePath
import os

def run_piece(
        image_path: FilePath,
        image_title: str = None,
        image_description: str = None,
        id_as_output: bool = True,
        title_as_output: bool = True,
        description_as_output: bool = True,
        delete_hash_as_output: bool = True,
        url_as_output: bool = True
):
    
    load_dotenv()
    CLIENT_ID = os.environ.get("CLIENT_ID")

    return piece_dry_run(
        #local piece repository path
        repository_folder_path="../",

        #name of the piece
        piece_name="ImgurImageUploaderPiece",

        #values to the InputModel arguments
        piece_input={
            "image_path": image_path,
            "image_title":image_title,
            "image_description": image_description,
            "id_as_output": id_as_output,
            "title_as_output": title_as_output,
            "description_as_output": description_as_output,
            "delete_hash_as_output": delete_hash_as_output,
            "url_as_output": url_as_output,
        },
        
        #values to the SecretModel arguments
        secrets_input={ 
            "CLIENT_ID": CLIENT_ID,
        }
)

def test_piece():
    piece_kwargs = {
        "image_path": "",
        "image_title": "image title",
        "image_description": "image description",
        "id_as_output": True,
        "title_as_output": True,
        "title_as_output": True,
        "description_as_output": True,
        "delete_hash_as_output": True,
        "url_as_output": True,
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["id_as_output"]: 
        assert output.image_id != None
    if piece_kwargs["title_as_output"]: 
        assert output.image_title == piece_kwargs["image_title"]
    if piece_kwargs["description_as_output"]: 
        assert output.image_description == piece_kwargs["image_description"]
    if piece_kwargs["delete_hash_as_output"]: 
        assert output.image_delete_hash != None
    if piece_kwargs["url_as_output"]: 
        assert output.image_url != None

if __name__ == "__main__":
    test_piece()
