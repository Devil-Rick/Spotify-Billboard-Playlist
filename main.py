from bs4 import BeautifulSoup
from datetime import date as dt
from datetime import datetime
import requests as req
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


today = str(dt.today())
date = input("Date on which you want to have Billboard Top 100 (YYYY-MM-DD) format: ")

if check_date(today, date):
    req_url = f"https://www.billboard.com/charts/hot-100/{date}/"
    print(top100(req_url))
else:
    print("Check the Date entered")
