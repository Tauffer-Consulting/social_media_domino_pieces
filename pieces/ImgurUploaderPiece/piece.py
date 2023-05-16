from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from imgurpython import ImgurClient
import time

class ImgurUploaderPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        client_id = self.secrets.CLIENT_ID
        client_secret = self.secrets.CLIENT_SECRET

        client = ImgurClient(client_id, client_secret)

        self.logger.info(f"Uploading image from {input_model.image_path}")

        upload_response = client.upload_from_path(path=input_model.image_path)

        time.sleep(2)

        self.logger.info("Image uploaded")

        return OutputModel(
            image_url = upload_response['link']
        )