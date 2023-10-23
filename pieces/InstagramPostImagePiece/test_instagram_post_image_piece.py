from domino.testing import piece_dry_run
from dotenv import load_dotenv
import os
import re

def run_piece(
        image_url: str,
        facebook_page_name: str,
        caption_header: str = None,
        caption: str = None,
        caption_footer: str = None,

):
    
    load_dotenv()
    APP_ID = os.environ.get("APP_ID")
    APP_SECRET = os.environ.get("APP_SECRET")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

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
            "APP_ID": APP_ID,
            "APP_SECRET": APP_SECRET,
            "ACCESS_TOKEN": ACCESS_TOKEN,
        }
)


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
    
    assert re.match(id_pattern, output.post_id)
    assert re.match(link_pattern, output.post_link)
