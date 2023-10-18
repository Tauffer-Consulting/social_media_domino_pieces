from domino.testing import piece_dry_run

def run_piece(
        url: str,
        output_type: str,
):
    
    return piece_dry_run(    
        #local piece repository path
        repository_folder_path="../",

        #name of the piece
        piece_name="YoutubeDownloadPiece",

        #values to the InputModel arguments
        piece_input={
            "url": url,
            "output_type": output_type
        },
)


def test_youtube_download_piece():
    piece_kwargs = {
        "url": "https://www.youtube.com/watch?v=zhWDdy_5v2w&ab_channel=AsapSCIENCE",
        "output_type": "audio"
    }
    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["output_type"] == "audio":
        assert output.file_path.endswith(".mp3")
    if piece_kwargs["output_type"] == "video":
        assert output.file_path.endswith(".mp4")
