from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("YT_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)


def print_json(data_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(data_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.youtube = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.youtube["items"][0]["snippet"]["title"]
        self.description = self.youtube["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + self.channel_id
        self.subscribers_count = int(self.youtube["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(self.youtube["items"][0]["statistics"]["videoCount"])
        self.views_count = int(self.youtube["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.views_count + other.views_count

    def __sub__(self, other):
        return self.views_count - other.views_count

    def __lt__(self, other):
        return self.views_count < other.views_count

    def __le__(self, other):
        return self.views_count <= other.views_count

    def __gt__(self, other):
        return self.views_count > other.views_count

    def __ge__(self, other):
        return self.views_count >= other.views_count

    def __eq__(self, other):
        return self.views_count == other.views_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        return print_json(self.youtube)

    @staticmethod
    def get_service():
        return youtube

    def to_json(self, path):
        directory = "../data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = os.path.join(directory, path)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data.append({
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers_count": self.subscribers_count,
            "video_count": self.video_count,
            "views_count": self.views_count,
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
