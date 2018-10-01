import logging
import requests

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_urls_from_href(base_url, save='data/urls_from_lg_database.txt'):
    links = []
    page = urlopen(Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})).read()
    soup = BeautifulSoup(page, 'html.parser')
    soup.prettify()

    for anchor in soup.findAll('a', href=True):
        if anchor.has_attr('title'):
            if anchor['title'][:4] == 'http':
                links.append(anchor['href'])
    print(links[:10])
    with open(save, 'w') as f:
        for item in links:
            f.write("%s\n" % item)


def get_urls_from_text(base_path, save_path):
    with open(base_path, 'r') as f:
        lines = f.read().splitlines()
    lines = lines[1:]
    urls = [line.split()[0] for line in lines]
    with open(save_path, 'w') as f:
        for item in urls:
            f.write("%s\n" % item)


def main():
    url_summary = 'data/LG_working_BGPSUM_IMC2013.txt'
    url_neighbors = 'data/LG_working_BGPNeighbors_IMC2013.txt'
    url_lg_database = 'http://www.bgplookingglass.com'

    save_summary = 'data/urls_from_bgpsum.txt'
    save_neighbors = 'data/urls_from_bgpneighbors.txt'

    # get_urls_from_href(url_lg_database)
    get_urls_from_text(url_summary, save_summary)
    get_urls_from_text(url_neighbors, save_neighbors)

if __name__ == "__main__":
    main()