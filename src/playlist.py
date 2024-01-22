import datetime

from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("YT_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        self.youtube = youtube.playlists().list(part='snippet', id=self.playlist_id).execute()
        self.title = self.youtube['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.videos = []

        playlist_items = youtube.playlistItems().list(part='contentDetails', playlistId=self.playlist_id,
                                                      maxResults=50).execute()
        for item in playlist_items.get('items', []):
            video_id = item['contentDetails']['videoId']
            self.videos.append(video_id)

    @property
    def total_duration(self) -> datetime.timedelta:
        total_duration = datetime.timedelta(seconds=0)

        for video_id in self.videos:
            videos_info = youtube.videos().list(
                part='contentDetails',
                id=video_id
            ).execute()

            if 'items' in videos_info:
                duration_str = videos_info['items'][0]['contentDetails']['duration']

                duration = datetime.timedelta()
                time = duration_str.split('T')
                if len(time) == 2:
                    if 'H' in time[1]:
                        hours, rest = time[1].split('H')
                        duration += datetime.timedelta(hours=int(hours))
                        time[1] = rest
                    if 'M' in time[1]:
                        minutes, rest = time[1].split('M')
                        duration += datetime.timedelta(minutes=int(minutes))
                        time[1] = rest
                    if 'S' in time[1]:
                        seconds = time[1].replace('S', '')
                        duration += datetime.timedelta(seconds=int(seconds))

                total_duration += duration

        return total_duration

    def show_best_video(self) -> str:
        if not self.videos:
            return "No videos in the playlist"

        best_video_id = ''
        best_likes = 0

        for video_id in self.videos:
            videos_info = youtube.videos().list(part='statistics', id=video_id).execute()

            if 'items' in videos_info:
                likes = int(videos_info['items'][0]['statistics']['likeCount'])

                if likes > best_likes:
                    best_likes = likes
                    best_video_id = video_id

        return f'https://www.youtube.com/{best_video_id}'
