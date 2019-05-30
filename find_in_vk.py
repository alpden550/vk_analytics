import datetime
import os
import requests
import argparse
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


def get_mentions_in_vk(search, start_time, end_time, method='newsfeed.search'):
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
        return None
    return response.json().get('response').get('total_count')


def get_timestamps(days=7):
    today = datetime.datetime.today().date()
    timestamps = []

    for day in range(1, days + 1):
        yesterday = today - datetime.timedelta(days=day)
        timestamp_start = datetime.datetime(
            yesterday.year,
            yesterday.month,
            yesterday.day,
            hour=0,
            minute=0).timestamp()
        timestamp_end = datetime.datetime(
            yesterday.year,
            yesterday.month,
            yesterday.day,
            hour=23,
            minute=59).timestamp()
        timestamps.append((datetime.date(yesterday.year, yesterday.month, yesterday.day),
                           timestamp_start,
                           timestamp_end))
    return timestamps


def get_day_mention(timestamps, search):
    statistics = []
    for day in timestamps:
        date, start_day, end_day = day
        mention = get_mentions_in_vk(search=search, start_time=start_day, end_time=end_day)
        statistics.append((date, mention))
    return statistics


def create_graph(statistics, graph_name='Graph'):
    x = [date for date, mentions in statistics]
    y = [mentions for date, mentions in statistics]
    trace = go.Bar(
        x=x,
        y=y
    )

    py.plot([trace], filename=f'{graph_name} mentions in VK', auto_open=True)


def create_parser():
    parser = argparse.ArgumentParser(description='Get mentions in VK from exactly period')
    parser.add_argument('search', help='Enter what to find')
    parser.add_argument('-p', '--period', help='Enter period', type=int)
    return parser.parse_args()


if __name__ == "__main__":
    parser = create_parser()
    timestamps = get_timestamps(days=parser.period)
    statistics = get_day_mention(timestamps, parser.search)
    create_graph(statistics)
