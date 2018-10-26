import requests 
from ast import literal_eval
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib

def send_pst_req(url_data):
    print(url_data[0])
    print(url_data[1])
    r = requests.post(url = url_data[0], data = url_data[1]) 
    return r.text

def send_get_req(url):
    r = requests.get(url)
    return r.text

def read_url_data(filepath):
    data = {}
    with open(filepath) as f:
        url = f.readline().strip()
        method = f.readline().strip()
        if method == 'post':
            for line in f.readlines():
                key, val = line.split(':')
                data[key] = val.strip()
            resp = send_pst_req([url, data])
        elif method == 'get':
            resp = send_get_req(url)
    return resp
        
    

    
if __name__ == "__main__":
    url = 'https://lg.as7012.net'
    answer = 'https://lg.as7012.net/cgi-bin/bgplg?cmd=show+ip+bgp+summary&req='
    r = requests.get(url)
    r_text = r.text
    soup = BeautifulSoup(r_text, 'html.parser')
    form = soup.find_all('form')[0]
    if 'method' in form.attrs:
        method = form.attrs['method']
    else:
        method = 'GET'
        
    endpoint = form.attrs['action']
    
    if method.upper() == 'POST':
        post_url = urljoin(url, endpoint)
        data = {}
        names = form.find_all('input')
        for name in names:
            if 'name' in name.attrs:
                key = name.attrs['name']
                if 'value' in name.attrs:
                    val = name.attrs['value']
                else:
                    val = ''
                data[key] = val
                
        select = form.find('select')
        key = select.attrs['name']
        options = select.find_all('option')
        for option in options:
            value = option.attrs['value']   
            if ('sum' in value) and ('6' not in value) and ('bgp' in value):
                val = value
                break
        data[key] = val
        a=send_pst_req([post_url, data])
    elif method.upper() == 'GET':
        get_url = urljoin(url, endpoint)+'?'
        data = {}
        select = form.find('select')
        key = select.attrs['name']
        options = select.find_all('option')
        for option in options:
            value = option.attrs['value']   
            if ('sum' in value) and ('6' not in value) and ('bgp' in value):
                val = value
                break
        data[key] = val
        
        names = form.find_all('input')
        for name in names:
            if 'name' in name.attrs:
                key = name.attrs['name']
                if 'value' in name.attrs:
                    val = name.attrs['value']
                else:
                    val = ''
                data[key] = val
        
        for item in data:
            get_url += item +'='+ urllib.parse.quote_plus(data[item]) +'&'
            
        a = send_get_req(get_url)