from domino.testing import piece_dry_run
from pydantic import FilePath
import os
import pytest

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

    IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")

    return piece_dry_run(
        #name of the piece
        piece_name="ImgurImageUploaderPiece",

        #values to the InputModel arguments
        input_data={
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
        secrets_data={ 
            "IMGUR_CLIENT_ID": IMGUR_CLIENT_ID,
        }
)

@pytest.mark.skip(reason="")
def test_imgur_image_uploader_piece():
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
        assert output.get("image_id") != None
    if piece_kwargs["title_as_output"]: 
        assert output.get("image_title") == piece_kwargs["image_title"]
    if piece_kwargs["description_as_output"]: 
        assert output.get("image_description") == piece_kwargs["image_description"]
    if piece_kwargs["delete_hash_as_output"]: 
        assert output.get("image_delete_hash") != None
    if piece_kwargs["url_as_output"]: 
        assert output.get("image_url") != None
