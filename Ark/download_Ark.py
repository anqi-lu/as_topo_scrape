import requests
from bs4 import BeautifulSoup
import urllib.request
import concurrent.futures
import gzip, os

#from start url to extract all urls to download ark info
#return a list of urls ready for downloading
def loop_url(start_url):
    url_list = []
    url_list.append(start_url + "team-1/2007/")
    for i in range(1,4):
        for j in range(2008, 2019):
            url_list.append(start_url + "team-" + str(i) + "/" + str(j) + "/")
    return url_list

# extract all the downloadable gz files from this url and store the AS pairs into as_dict
# the pair is stored in the form: 123 3456 (previous < latter, divided by semi-coma)
def download_gz_files(url_list, read_root):
    for url in url_list:
        r = requests.get(url, timeout=10)
        html = r.content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html, 'html.parser')
        end_point_list = soup.find_all('a')
        for i in range(5, len(end_point_list)):
            endpoint = end_point_list[i]['href']
            download_url = url + endpoint
            # read_root = 'Ark/download/'
            urllib.request.urlretrieve(download_url, read_root + endpoint)
    return

def store_as_pairs(read_root, store_root, as_dict):
    file_names = os.listdir(read_root)
    for file_name in file_names:
        file_path = os.path.join(read_root, file_name)
        with gzip.open(file_path, 'rb') as f:
            content = f.readlines()
            for line in content:
                if line[0] == 68:
                    as_pair = line.split(b'\t')
                    if (isInt(as_pair[1]) and isInt(as_pair[2])):
                        store_as_tuple(int(as_pair[1]), int(as_pair[2]), as_dict)
    for as_pair_tuple in as_dict:
        with open(store_root, 'a') as f:
            f.write(as_pair_tuple + '\n')

def store_as_tuple(as_1, as_2, as_dict):
    if as_1 < as_2:
        as_min = as_1
        as_max = as_2
    else:
        as_min = as_2
        as_max = as_1
    if(len(str(as_min)) > 6 or len(str(as_max)) > 6):
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
    start_url = 'http://data.caida.org/datasets/topology/ark/ipv4/as-links/'
    read_root = 'download/'
    store_root = 'Ark_AS_pairs.txt'
    as_dict = set()
    url_list = loop_url(start_url)
    download_gz_files(url_list, read_root)
    store_as_pairs(read_root, store_root, as_dict)
    return


if __name__ == "__main__":
    main()


    # with concurrent.futures.ProcessPoolExecutor() as executor: 
    #     executor.map(download_url, lis[5:])
        
    
    