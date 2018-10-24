import requests 
from ast import literal_eval
from bs4 import BeautifulSoup

def send_pst_req(url_data):
    r = requests.post(url = url_data[0], data = url_data[1]) 
    return r.text

def read_url_data(filepath):
    response=[]
    with open(filepath) as f:
        url = ''
        for line in f.readlines():
            if line[:4] == 'http':
                if len(url) > 0:
                    send_pst_req([url, data])
                    response.append(resp)
                url = line.strip()
                data = {}
            else:
                (key, val) = line.split(':')
                data[key] = val.strip()
        resp = send_pst_req([url, data])
        response.append(resp)
    return response
        
    

    
if __name__ == "__main__":
    a=read_url_data('data/bgp_summ_request_url_data.txt')
    