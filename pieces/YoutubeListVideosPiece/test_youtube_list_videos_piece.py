from domino.testing import piece_dry_run
from datetime import date, datetime
import os
import pytest



def run_piece(
    channel_username: str,
    max_videos: int = 10,
    published_at_or_after: date = None,
    published_at_or_before: date = None,
    order_by: str = "date",
    video_duration: str = "any",
):
    
    
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
    
    return piece_dry_run(    
        #name of the piece
        piece_name="YoutubeListVideosPiece",

        #values to the InputModel arguments
        input_data={
            "channel_username": channel_username,
            "max_videos": max_videos,
            "published_at_or_after": published_at_or_after,
            "published_at_or_before": published_at_or_before,
            "order_by": order_by,
            "video_duration": video_duration,
        },

        secrets_data={
            "YOUTUBE_API_KEY": YOUTUBE_API_KEY
        }
)

@pytest.mark.skip(reason="")
def test_youtube_list_videos_piece():
    piece_kwargs = {
        "channel_username": "bbcnews",
        "max_videos": 20,
        "published_at_or_after": datetime.strptime("2023-11-01", "%Y-%m-%d").date(),
        "published_at_or_before": None,
        "order_by": "date",
        "video_duration": "any",
    }
    output = run_piece(
        **piece_kwargs
    )

    if piece_kwargs["max_videos"]:
        assert len(output.get("videos_list")) <= piece_kwargs["max_videos"]
    if piece_kwargs["published_at_or_after"]:
        for video in output.get("videos_list"):
            published_at = datetime.strptime(video["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").date()
            assert published_at >= piece_kwargs["published_at_or_after"]
    if piece_kwargs["published_at_or_before"]:
        for video in output.get("videos_list"):
            published_at = datetime.strptime(video["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").date()
            assert published_at <= piece_kwargs["published_at_or_before"]
    if piece_kwargs["order_by"] == "date":
        assert output.get("videos_list") == sorted(output.get("videos_list"), key=lambda x: datetime.strptime(x["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    if piece_kwargs["order_by"] == "title":
        assert output.get("videos_list") == sorted(output.get("videos_list"), key=lambda x: x["title"])
    if piece_kwargs["order_by"] == "viewCount":
        assert output.get("videos_list") == sorted(output.get("videos_list"), key=lambda x: int(x["viewCount"]), reverse=True)
