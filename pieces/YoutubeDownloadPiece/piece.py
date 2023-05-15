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
            options={
                "format": "bestaudio/best",
                "keepvideo": False,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }]
            }
            file_format = ".mp3"
        else:
            options={
                "format": "bestvideo+bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4"
                }]
            }
            file_format = ".mp4"
        
        # File name
        video_info = youtube_dl.YoutubeDL().extract_info(url=input_model.url, download=False)
        if input_model.output_file_name:
            filename = f"{input_model.output_file_name}"
        else:
            filename = f"{video_info['title']}"

        output_file_path = f"{self.results_path}/{filename}"
        options['outtmpl'] = output_file_path
        output_file_path += file_format

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
