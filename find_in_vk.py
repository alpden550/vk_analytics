import datetime
import os
import requests
from dotenv import load_dotenv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


load_dotenv()

ACCESS_TOKEN = os.getenv('VK_KEY')
VK_API = 'https://api.vk.com/method/'
VERSION = 5.95
PLOTLY_USERNAME = os.getenv('PLOTLY_NAME')
PLOTLY_KEY = os.getenv('PLOTLY_KEY')

plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_KEY)


def find_mentions(search, start_time, end_time, method='newsfeed.search'):
    parameters = {
        'access_token': ACCESS_TOKEN,
        'v': VERSION,
        'q': search,
        'start_time': start_time,
        'end_time': end_time,
    }
    url = f'{VK_API}{method}'
    response = requests.get(url, params=parameters)
    if 'error' in response.json():
        # raise requests.HTTPError(response.json()['error'])
        return None
    return response.json().get('response').get('total_count')


def get_timestamps(days=7):
    today = datetime.datetime.today().date()
    timestamps = []

    for day in range(1, days + 1):
        yesterday = today - datetime.timedelta(days=day)
        timestamp_start = datetime.datetime(
            yesterday.year, yesterday.month, yesterday.day).timestamp()
        timestamp_end = datetime.datetime(
            yesterday.year, yesterday.month, yesterday.day + 1).timestamp()
        timestamps.append((datetime.date(yesterday.year, yesterday.month, yesterday.day),
                           timestamp_start,
                           timestamp_end))

    return timestamps


def get_day_mention(timestamps, search):
    statistics = []
    for day in timestamps:
        mention = find_mentions(search=search, start_time=day[1], end_time=day[2])
        statistics.append((day[0], mention))
    return statistics


if __name__ == "__main__":
    timestamps = get_timestamps()
    statistics = get_day_mention(timestamps, 'Coca Cola')
    x, y = [], []

    for day in statistics:
        x.append(day[0])
        y.append(day[1])

    trace = go.Bar(
        x=x,
        y=y
    )
    data = [trace]
    py.plot(data, filename='basic-bar', auto_open=True)
