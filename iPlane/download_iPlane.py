import requests
from bs4 import BeautifulSoup
import urllib.request
import concurrent.futures
import gzip, os
import re

# request from url like: http://web.eecs.umich.edu/~harshavm/iplane/iplane_logs/data/2011/01/01/pl_traceroutes/curr_inter_ip_links.txt
def url_generator(base_url,start_y, end_y, file_name):
    url_list = []
    for y in range(start_y, end_y + 1):
        for m in range(1, 13):
            for d in range(1, 32):
                curr_url = base_url + str(y) + '/' + format(m, '02d') + '/' + format(d, '02d') + '/' + file_name
                if url_is_alive(curr_url):
                    url_list.append(curr_url)
    return url_list

def url_is_alive(url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

# extract all the downloadable txt files from url list into download folder
def download_txt_files(url_list, txt_root):
    i = 1
    for url in url_list:
        filename = str(i) + '.txt'
        urllib.request.urlretrieve(url, filename)
        i = i + 1
    return

# loop through all the files in the download and store as pairs
# the pair is stored in the form: 123 3456 (previous < latter, divided by semi-coma)
def store_as_pairs(read_root, store_name, as_dict):
    file_names = os.listdir(read_root)
    for file_name in file_names:
        file_path = os.path.join(read_root, file_name)
        with open(file_path, 'r') as f:
            content = f.readlines()
            for line in content:
                info = line.split()
                if len(info) < 4:
                    continue
                elif isInt(info[1]) and isInt(info[3]):
                    as_1 = int(info[1])
                    as_2 = int(info[3])
                    store_as_tuple(as_1, as_2, as_dict)

    for as_tuple in as_dict:
        with open(store_name, 'a') as f:
            f.write(as_tuple + '\n')
    return

def store_as_tuple(as_1, as_2, as_dict):
    if as_1 < as_2:
        as_min = as_1
        as_max = as_2
    else:
        as_min = as_2
        as_max = as_1
    if len(str(as_min)) > 6 or len(str(as_max)) > 6:
        return
    as_dict.add(str(as_min) + "," + str(as_max))
    return


def isInt(num):
    try:
        int(num)
        return True
    except:
        return False

def main():
    # url_base = 'http://web.eecs.umich.edu/~harshavm/iplane/iplane_logs/data/'
    read_root = 'download/'
    store_name = 'iPlane_AS_pairs.txt'
    as_dict = set()
    url_list = url_generator(url_base,2011, 2016, 'pl_traceroutes/curr_inter_ip_links.txt')
    download_txt_files(url_list, read_root)
    store_as_pairs(read_root, store_name, as_dict)

if __name__ == "__main__":
    main()
        
    
    