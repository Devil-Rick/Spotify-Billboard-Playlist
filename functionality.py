from bs4 import BeautifulSoup
import pprint
from datetime import datetime
import requests as req
import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re


def check_date(today_date, curr_date):
    try:
        ok = False
        if datetime.strptime(today_date, "%Y-%m-%d") >= datetime.strptime(curr_date, "%Y-%m-%d"):
            ok = True
    except ValueError:
        print("Check the Date entered")
    else:
        return ok


def top100(url):
    response_url = req.get(url).text
    soup = BeautifulSoup(response_url, "html.parser")
    top_100 = []
    for title in soup.select(selector="li #title-of-a-story"):
        data = title.get_text()
        data = re.sub(r'[\t\n ]+', ' ', data).strip()
        top_100.append(data)
    return top_100


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIFY_ID,
                                                            client_secret=config.SPOTIFY_KEY,
                                                            redirect_uri=config.SPOTIFY_URL,
                                                            scope=config.SPOTIFY_SCOPE))
        self.song_list = []
        self.id = ""
        self.playlist_id = ""

    def user_data(self):
        user = self.sp.current_user()
        self.id = user["id"]
        return user

    def get_tracks(self, all_track):
        for track in all_track:
            track_id = self.sp.search(q=track, limit=1, type='track')
            track_name = track
            track_uri = track_id["tracks"]["items"][0]["uri"]
            self.song_list.append({"track": track_name,
                                   "uri": track_uri})

    def create_playlist(self, date):
        self.user_data()
        new_playlist = self.sp.user_playlist_create(user=self.id,
                                                    name=f"{date} BillBoard Top 100",
                                                    description="Contains top 100 Billboard Songs",
                                                    public=False)
        self.playlist_id = new_playlist["id"]

    def add_tracks(self):
        track_uri_list = [song["uri"] for song in self.song_list]
        self.sp.playlist_add_items(playlist_id=self.playlist_id, items=track_uri_list)

    def print_tracks(self):
        pprint.pprint(self.song_list)
