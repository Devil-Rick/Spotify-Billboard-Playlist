from datetime import date as dt
import functionality as func

today = str(dt.today())
date = input("Date on which you want to have Billboard Top 100 (YYYY-MM-DD) format: ")

if func.check_date(today, date):
    req_url = f"https://www.billboard.com/charts/hot-100/{date}/"
    track_list = func.top100(req_url)
    spotify = func.Spotify()
    spotify.get_tracks(track_list)
else:
    print("Check the Date entered")
