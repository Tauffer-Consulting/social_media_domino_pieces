"""
References:
- https://github.com/ytdl-org/youtube-dl
"""
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import yt_dlp as youtube_dl
import os
from typing import List


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

        file_size = os.path.getsize(output_file_path) *  0.000001
        
        # Display result in the Domino GUI
        self.format_display_result(input_model, video_info, file_size)

        return OutputModel(
            message=msg,
            file_path=output_file_path
        )
    
    def format_display_result(self, input_model: InputModel, video_info: List, file_size: int):
        md_text = f"""
## Information about the video

- Title: {video_info['title']}
- Duration: {video_info['duration']} seconds
- Link: [{video_info['webpage_url']}]({video_info['webpage_url']}   )
- Vizualizations: {video_info['view_count']}
- Resolution:  {video_info['resolution']}
- Downloaded file size: {round(file_size, 3)} MB

"""
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
