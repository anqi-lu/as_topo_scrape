import logging
import concurrent.futures

from download import get_data

def fetch_all(urls):
    """This will download all the pages from the responses. 
    
    This makes conccurent async requests and utilizes all available cores,
    to reduce runtime.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor: 
        successes = executor.map(_get_data_task, urls)

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

def _get_data_task(url):
    """Task which wraps the get_data function and returns a 1 on success and 0 otherwise. """
    if get_data(url) is None:
        return 0
    return 1

def get_urls(file_path):
    with open(file_path, 'r') as f:
        urls = f.read().splitlines()
    return urls

def main():
    lg_summary = 'data/urls_from_bgpsum.txt'
    lg_neighbor = 'data/urls_from_bgpneighbors.txt'

    lg_database = 'data/urls_from_lg_database.txt'
    
    # fetch_all(get_urls(lg_database))
    # fetch_all(get_urls(lg_summary))
    fetch_all(get_urls(lg_neighbor))

if __name__ == "__main__":
    main()