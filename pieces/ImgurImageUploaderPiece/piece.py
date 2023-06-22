from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import time
import base64
import requests
import json


class ImgurImageUploaderPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        client_id = self.secrets.CLIENT_ID

        with open(input_model.image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        payload = {
            "image": encoded_string,
            "title": input_model.image_title if input_model.image_title else "",
            "description": input_model.image_description if input_model.image_description else "",
        }
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

        output_map = {
            "id_as_output":{"imgur_param":"id", "output_model_param":"image_id"}, 
            "title_as_output":{"imgur_param":"title", "output_model_param":"image_title"}, 
            "description_as_output":{"imgur_param":"description", "output_model_param":"image_description"},
            "delete_hash_as_output":{"imgur_param":"deletehash", "output_model_param":"image_delete_hash"}, 
            "url_as_output":{"imgur_param":"link", "output_model_param":"image_url"},
        }

        input_model_args = json.loads(input_model.json())
        selected_output_params = {key:output_map[key]["imgur_param"] for key, value in input_model_args.items() if value==True}
        output_kwargs = {output_map[key]["output_model_param"]:image_data["data"][value] for key, value in selected_output_params.items()}

        # Display result in the Domino GUI
        self.format_display_result(image_data["data"])

        return OutputModel(
            **output_kwargs
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