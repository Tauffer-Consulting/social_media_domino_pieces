"""
References:
- https://github.com/ytdl-org/youtube-dl
"""
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import yt_dlp as youtube_dl


class YoutubeDownloadPiece(BasePiece):

    def piece_function(self, input_model: InputModel):
        # File type
        if input_model.output_type == "audio":
            format = "bestaudio/best"
            file_ext = "mp3"
        else:
            format = "bestvideo+bestaudio/best"
            file_ext = "mp4"

        # File name
        video_info = youtube_dl.YoutubeDL().extract_info(url=input_model.url, download=False)
        if input_model.output_file_name:
            filename = f"{input_model.output_file_name}.{file_ext}"
        else:
            filename = f"{video_info['title']}.{file_ext}"

        output_file_path = f"{self.results_path}/{filename}"
        options={
            'format': format,
            'keepvideo': False,
            'outtmpl': output_file_path,
        }

        # Download the content
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        msg = f"Download complete successfully: {filename}"
        self.logger.info(msg)

        output = OutputModel(
            message=msg,
            file_path=output_file_path
        )

        return output
