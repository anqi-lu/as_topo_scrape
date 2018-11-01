from download import get_data
from fetch import get_urls
from post_get_request import send_request
import datetime


if __name__ == "__main__":
    lg_summary = 'data/urls_from_bgpsum.txt'
    lg_neighbor = 'data/urls_from_bgpneighbors.txt'

    lg_database = 'data/urls_from_lg_database.txt'
    urls = get_urls(lg_summary)
    for i, url in enumerate(urls):
        if get_data(url):
            try:
                send_request(url)

            except ValueError as err:
                with open('error_url.txt', 'a') as f:
                    f.write(err.args[0]+'\n'+url+'\n')
                print(err.args)
            