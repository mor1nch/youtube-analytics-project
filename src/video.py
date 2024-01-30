from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("YT_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.youtube = None
        self.title = None
        self.link_to_video = None
        self.views_amount = None
        self.likes_amount = None

        try:
            self.youtube = youtube.videos().list(part='snippet,statistics', id=self.video_id).execute()
            self.title = self.youtube["items"][0]["snippet"]["title"]
            self.link_to_video = f'https://www.youtube.com/watch?v={self.video_id}'
            self.views_amount = int(self.youtube["items"][0]["statistics"]["viewCount"])
            self.likes_amount = int(self.youtube["items"][0]["statistics"].get("likeCount", 0))
        except IndexError:
            print('Передан несуществующий id видео')

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
