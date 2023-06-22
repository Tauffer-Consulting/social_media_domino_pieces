from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import time
import requests


class ImgurDeleteImagePiece(BasePiece):
    def piece_function(self, input_model: InputModel):
        access_token = self.secrets.ACCESS_TOKEN
        image_delete_hash = input_model.image_delete_hash

        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://api.imgur.com/3/image/{image_delete_hash}"
        try:
            response = requests.delete(url=url, headers=headers)
        except Exception as e:
            self.logger.info(f"Deletion failed: {e}")
            raise Exception(f"Deletion failed: {e}")

        time.sleep(2)

        self.logger.info("Image deleted")

        # Display result in the Domino GUI
        self.format_display_result(response.status_code)

        return OutputModel(
            deletion_status=response.status_code
        )
    
    def format_display_result(self, response_status: int):
        md_text = f"""
## Response status of image deletion:  

{response_status}  
"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }