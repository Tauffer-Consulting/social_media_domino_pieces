from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from imgurpython import ImgurClient

class ImgurUploaderPiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        client_id = self.secrets.CLIENT_ID
        client_secret = self.secrets.CLIENT_SECRET

        client = ImgurClient(client_id, client_secret)

        upload_response = client.upload_from_path(path=input_model.image_path)

        return OutputModel(
            image_url = upload_response['link']
        )