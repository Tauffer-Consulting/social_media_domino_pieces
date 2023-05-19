from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from imgurpython import ImgurClient
import time

class ImgurUploaderPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        client_id = self.secrets.CLIENT_ID
        client_secret = self.secrets.CLIENT_SECRET

        self.logger.info(f"Uploading image from {input_model.image_path}")

        try:
            client = ImgurClient(client_id, client_secret)
            upload_response = client.upload_from_path(path=input_model.image_path)
        except Exception as e:
            self.logger.info(f"Upload failed: {e}")
            raise Exception(f"Upload failed: {e}")

        time.sleep(2)

        self.logger.info("Image uploaded")
        
        image_url = upload_response['link']

        # Display result in the Domino GUI
        self.format_display_result(input_model, image_url)

        return OutputModel(
            image_url=image_url
        )
    
    def format_display_result(self, input_model: InputModel, image_url: str):
        md_text = f"""
## Uploaded image link from Imgur:
{image_url}

"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }