from domino.testing import piece_dry_run
import pytest
import os
import re

def run_piece(
    image_url: str,
    facebook_page_name: str,
    caption_header: str = None,
    caption: str = None,
    caption_footer: str = None,
):
    
    
    INSTAGRAM_APP_ID = os.environ.get("INSTAGRAM_APP_ID")
    INSTAGRAM_APP_SECRET = os.environ.get("INSTAGRAM_APP_SECRET")
    INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")

    return piece_dry_run(    
        #name of the piece
        piece_name="InstagramPostImagePiece",

        #values to the InputModel arguments
        input_data={
            "image_url": image_url,
            "caption_header": caption_header,
            "caption": caption,
            "caption_footer": caption_footer,
            "facebook_page_name": facebook_page_name
        },
            
        #values to the SecretModel arguments
        secrets_data={ 
            "INSTAGRAM_APP_ID": INSTAGRAM_APP_ID,
            "INSTAGRAM_APP_SECRET": INSTAGRAM_APP_SECRET,
            "INSTAGRAM_ACCESS_TOKEN": INSTAGRAM_ACCESS_TOKEN,
        }
)

@pytest.mark.skip(reason="")
def test_instagram_post_image_piece():
    output = run_piece(
        image_url="",
        facebook_page_name="",
        caption_footer="",
        caption="",
        caption_header=""
    )
    
    # Regex pattern for matching only numbers
    id_pattern = r'^\d+$'
    link_pattern = r'^https://www\.instagram\.com/p/.+$'
    
    assert re.match(id_pattern, output.get('post_id'))
    assert re.match(link_pattern, output.get('post_link'))
