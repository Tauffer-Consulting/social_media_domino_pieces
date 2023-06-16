from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from imgurpython import ImgurClient
import time
import base64
import requests


class ImgurImageUploaderPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        client_id = self.secrets.CLIENT_ID
        client_secret = self.secrets.CLIENT_SECRET

        with open(input_model.image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        payload = {"image": encoded_string}
        headers = {"Authorization": f"Client-ID {client_id}"}

        self.logger.info(f"Uploading image from {input_model.image_path}")

        try:
            response = requests.post("https://api.imgur.com/3/image", data=payload, headers=headers)
        except Exception as e:
            self.logger.info(f"Upload failed: {e}")
            raise Exception(f"Upload failed: {e}")

        time.sleep(2)

        self.logger.info("Image uploaded")
        
        image_data = response.json()

        # Display result in the Domino GUI
        self.format_display_result(image_data["data"])

        return OutputModel(
            image_url=image_data["data"]['link'],
            image_delete_hash=image_data["data"]['deletehash']
        )
    
    def format_display_result(self, image_data: dict):
        md_text = f"""
## Uploaded image information from Imgur:  

"""
        for key, value in image_data.items():
            md_text += f"- {key}: {value}  \n"
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }