import logging
import concurrent.futures

from download import get_data
from post_get_request import send_request
import datetime

def fetch_all(urls, category):
    """This will download all the pages from the responses. 
    
    This makes conccurent async requests and utilizes all available cores,
    to reduce runtime.
    """
    parameters = [(url, category) for url in urls]

    with concurrent.futures.ProcessPoolExecutor() as executor: 
        successes = executor.map(_get_data_task, parameters)

    success_count = sum(successes)
    total_count = len(urls)
    _report(success_count, total_count)


def _report(success_count, total_count):
    """Logs percentage of success."""
    lost_count = total_count - success_count
    percent = success_count / (1. * lost_count + success_count)
    print("success_count: {}. lost_count: {}. percent: {}.".format(success_count, lost_count, percent))
    with open("data/output/fetch_report.txt", 'a') as f:
        f.write("success_count: {}. lost_count: {}. percent: {}.\n".format(success_count, lost_count, percent))

def _get_data_task(args):
    """Task which wraps the get_data function and returns a 1 on success and 0 otherwise. """
    url, category = args
    if get_data(url):
        try:
            text = send_request(url)
            dest = 'data/output/' + category + '/' + generate_name_from_url(url) '.txt'
            with open(dest, 'a') as f:
                f.write(url)
                f.write(text)
            return 1
        except ValueError as err:
            print(err.args)
            return 0
    else:
        return 0

def get_urls(file_path):
    with open(file_path, 'r') as f:
        urls = f.read().splitlines()
    return urls


def generate_name_from_url(url):
    if url[:5] == "https":
        url = url[8:]
    elif url[:4] == "http":
        url = url[7:]
    return url.replace("/", ".")

def main():
    lg_summary = 'data/urls_from_bgpsum.txt'
    lg_neighbor = 'data/urls_from_bgpneighbors.txt'
    lg_database = 'data/urls_from_lg_database.txt'
    
    # fetch_all(get_urls(lg_database), "database")
    fetch_all(get_urls(lg_summary), "summary")
    fetch_all(get_urls(lg_neighbor), "neighbor")

if __name__ == "__main__":
    main()