import json
import requests
from models import Media

media_dict = {}
CACHE_FILE_PATH = "./cache/cache_data.txt"


# load data from the cache file
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
    """using webAPI and the cached data to search the detail info of the movie

    Parameters
    ----------
    title: str
        the title of the movie

    Returns
    -------
    Media
        the detail information about the movie
    """
    if title in media_dict:
        return media_dict[title]

    para_dict = {"apikey": "a6004ed9", "t": title}
    resp = requests.get("http://www.omdbapi.com", para_dict)
    # create the Media object
    new_media = Media(resp.json())
    # if the object has a title, we need to cache the result
    if new_media.title:
        media_dict[title] = new_media
        # save data into the cache file
        with open(CACHE_FILE_PATH, "a+") as file:
            file.write(resp.text + "\n")
    return new_media
