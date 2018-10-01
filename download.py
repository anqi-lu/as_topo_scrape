import logging
import requests

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_data(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=10.) as data:
        # convert from bytearray to string.
            try:
                html = data.read().decode("utf8")
            except:
                logging.error("Failed to decode: {}".format(url))
                return None
    except:
        logging.error("Failed to download: {}".format(url))
        return None
    return True
