import requests
from bs4 import BeautifulSoup
import urllib.request
import concurrent.futures
import gzip, os
import re

# extract all the downloadable gz files from this url and store the AS pairs into as_dict
# the pair is stored in the form: 123 3456 (previous < latter, divided by semi-coma)
# def download_gz_files(url_list, read_root):
#     for url in url_list:
#         r = requests.get(url, timeout=10)
#         html = r.content.decode('utf-8', 'ignore')
#         soup = BeautifulSoup(html, 'html.parser')
#         end_point_list = soup.find_all('a')
#         for i in range(5, len(end_point_list)):
#             endpoint = end_point_list[i]['href']
#             download_url = url + endpoint
#             # read_root = 'Ark/download/'
#             urllib.request.urlretrieve(download_url, read_root + endpoint)
#     return

def store_as_pairs(read_root, store_root, as_dict):
    file_names = os.listdir(read_root)
    for file_name in file_names:
        file_path = os.path.join(read_root, file_name)
        with gzip.open(file_path, 'rb') as f:
            content = f.readlines()
            as_1 = -1
            for line in content:
                new_line = line.decode('ASCII', 'ignore')
                if "aut-num:" in new_line and isValid(new_line):
                    as_1 = findAS_in_string(new_line)
                elif ("export:" in new_line or "import:" in new_line) and isValid(new_line):
                    as_2 = findAS_in_string(new_line)
                    store_as_tuple(as_1, as_2, as_dict)

    for as_tuple in as_dict:
        with open('IRR_AS_pairs.txt', 'a') as f:
            f.write(as_tuple + '\n')
    return

def isValid(line):
    words = line.split("AS")
    prev = words[0]
    if len(words) < 2:
        return False
    elif not isInt(words[1].split()[0]):
        return False
    elif "aut-num:" in prev or "export:" in prev or "import:" in prev:
        return True    
    return False

def findAS_in_string(line):
    as_string = line.split("AS")[1]
    as_string = as_string.replace(":", " ")
    as_string = as_string.replace(";", " ")
    as_string = as_string.replace(",", " ")
    as_string = as_string.replace("_", " ")                 
    return int(as_string.split()[0].strip())

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
    as_dict = set()
    store_root = 'IRR_AS_pairs.txt'
    read_root = 'download/'
    store_as_pairs(read_root, store_root, as_dict)
    return

if __name__ == "__main__":
    main()
        
    
    