from domino.testing import piece_dry_run
import os
import pytest


def run_piece(
        facebook_page_name: str,
        output_type: str,
        id_field: bool = True,
        media_type_field: bool = True,
        caption_field: bool = True,
        like_count_field: bool = True,
        comments_count_field: bool = True,
        permalink_field: bool = True,
        timestamp_field: bool = True,
        comments_field: bool = True,
):
    
    INSTAGRAM_APP_ID = os.environ.get("INSTAGRAM_APP_ID")
    INSTAGRAM_APP_SECRET = os.environ.get("INSTAGRAM_APP_SECRET")
    INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")

    return piece_dry_run(    
        #name of the piece
        piece_name="InstagramGetMediaPiece",

        #values to the InputModel arguments
        input_data={
            "facebook_page_name": facebook_page_name,
            "output_type": output_type,
            "id_field": id_field,
            "media_type_field": media_type_field,
            "caption_field": caption_field,
            "like_count_field": like_count_field,
            "comments_count_field": comments_count_field,
            "permalink_field": permalink_field,
            "timestamp_field": timestamp_field,
            "comments_field": comments_field,
        },
        
        #values to the SecretModel arguments
        secrets_data={ 
            "INSTAGRAM_APP_ID": INSTAGRAM_APP_ID,
            "INSTAGRAM_APP_SECRET": INSTAGRAM_APP_SECRET,
            "INSTAGRAM_ACCESS_TOKEN": INSTAGRAM_ACCESS_TOKEN,
        }
)

@pytest.mark.skip(reason="")
def test_instagram_get_media_piece():
    piece_kwargs = {
        "facebook_page_name": "",
        "output_type": "python_list",
        "id_field": False,
        "media_type_field":True,
        "caption_field":True,
        "like_count_field":True,
        "comments_count_field":True,
        "permalink_field":True,
        "timestamp_field":True,
        "comments_field":True,
    }

    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "python_list":
        assert type(output.media_list) == list
        for item in output.get("media_list"):
            assert (key in item for key, value in piece_kwargs.items() if value == True)
            assert (key not in item for key, value in piece_kwargs.items() if value == False)
