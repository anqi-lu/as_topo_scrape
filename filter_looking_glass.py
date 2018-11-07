# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:54:20 2018

@author: genix
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fetch import get_urls
import requests
from download import get_data

def save_urls(base_url, save):
   
    urls = get_urls(base_url)
    for url in urls:
        if get_data(url):
            if find_looking_glass(url):
                with open(save, 'a') as f:
                    f.write("%s\n" % url)
    return None

def find_looking_glass(url):
    r = requests.get(url, timeout=10)
    while r.url != url:
        url = r.url
        r = requests.get(url)
    html = r.content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text().lower()
    if 'looking glass' in text or 'lg' in text:
        return True
    return False
    
    
def main():
    url_summary = 'data/urls_from_bgpneighbors.txt'
    url_neighbors = 'data/urls_from_bgpsum.txt'
    url_lg_database = 'data/urls_from_lg_database.txt'

    save_summary = 'data/urls_from_bgpsum.txt'
    save_neighbors = 'data/urls_from_bgpneighbors.txt'
    save_lg_dataset = 'data/urls_with_looking_glass.txt'

    save_urls(url_lg_database, save_lg_dataset)
    #print(find_looking_glass('https://lg.itsbrasil.net/'))

if __name__ == "__main__":
    main()
