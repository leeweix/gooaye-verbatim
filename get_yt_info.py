import os
import time
import requests
from datetime import datetime

class NoneValueError(Exception):
    pass

API_KEY = 'AIzaSyAVmMzBqtoBioFlz7ZB29EiAUvazDp0xU4'
CHANNEL_ID = 'UC23rnlQU_qE3cec9x709peA'

url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=50'

while True:
    response = requests.get(url)
    videos = response.json().get('items', [])

    # video_urls = []
    # First video is latest
    for video in videos:
        if video['id']['kind'] == 'youtube#video':
            # video_urls.append(f"https://www.youtube.com/watch?v={video['id']['videoId']}")
            break
    if not videos:
        print(videos)
        raise NoneValueError('Please check if video is void')
    
    # check publishTime is not in accorcance with previous one
    with open('publishTime.txt', 'r') as f:
        preTime = f.read()
    if video['snippet']['publishTime'] == preTime:
        print(datetime.now(),' No updated!')    
    else:
        with open('publishTime.txt', 'w+') as f:
            f.write(video['snippet']['publishTime'])
        with open('videoInfo.txt', 'w+') as f:
            f.writelines([video['snippet']['title']+'\n', video['id']['videoId']+'\n',  video['snippet']['publishTime']+'\n'])
        res = os.system(f"./yt-tldr.sh {video['id']['videoId']}")
        print(res)
        print(f"{datetime.now()} {video['snippet']['title']} is available!")
    time.sleep(3600)