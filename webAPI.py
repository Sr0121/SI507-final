import json
import requests
from models import Media

media_dict = {}
CACHE_FILE_PATH = "./cache/cache_data.txt"


def load_cache():
    try:
        with open(CACHE_FILE_PATH, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                new_media = Media(json.loads(line))
                media_dict[new_media.title] = new_media
    except FileNotFoundError:
        pass


def fetch_data(title):
    if title in media_dict:
        return media_dict[title]

    para_dict = {"apikey": "a6004ed9", "t": title}
    resp = requests.get("http://www.omdbapi.com", para_dict)
    with open(CACHE_FILE_PATH, "a+") as file:
        file.write(resp.text + "\n")
    new_media = Media(resp.json())
    media_dict[title] = new_media
    return new_media
