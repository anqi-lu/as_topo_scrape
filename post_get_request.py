import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib

# send post request, return html text results, need further data ectraction
def send_pst_req(url_data):
    r = requests.post(url = url_data[0], data = url_data[1]) 
    return r.text

#send get request, return html text results, need further data ectraction
def send_get_req(url):
    r = requests.get(url)
    return r.text

# =============================================================================
#         find option from <select> frame
#         option -> show ip bgp summary
#         find bgp summary option
# =============================================================================
def select_option_todata(form, data):
    select = form.find('select')
    key = select.attrs['name']
    options = select.find_all('option')
    for option in options:
        value = option.attrs['value']   
        if ('sum' in value) and ('6' not in value) and ('bgp' in value):
            val = value
            break
    data[key] = val
# =============================================================================
#         find from <input> frame
#         input -> (name , value)
#         find all names with its value
#         store (name:value) to data, if a name with no value, then value = ''
# =============================================================================
def input_name_todata(form, data):  
    inputs = form.find_all('input')
    for inp in inputs:
        if 'name' in inp.attrs:
            key = inp.attrs['name']
            if 'value' in inp.attrs:
                val = inp.attrs['value']
            else:
                val = ''
            data[key] = val
# =============================================================================
# def read_url_data(filepath):
#     data = {}
#     with open(filepath) as f:
#         url = f.readline().strip()
#         method = f.readline().strip()
#         if method == 'post':
#             for line in f.readlines():
#                 key, val = line.split(':')
#                 data[key] = val.strip()
#             resp = send_pst_req([url, data])
#         elif method == 'get':
#             resp = send_get_req(url)
#     return resp
# =============================================================================

#input AS source url, return html text
def send_request(url):
    #get form contents inside the html
    r = requests.get(url)
    r_text = r.text
    soup = BeautifulSoup(r_text, 'html.parser')
    #all the needed info is inside the [form] frame
    form = soup.find_all('form')[0]
    #determine method (GET or POST)
    if 'method' in form.attrs:
        method = form.attrs['method']
    else:
        method = 'GET'
        
    endpoint = form.attrs['action']
    #create data lib to store request info
    data = {}
    #if it's a post method
    if method.upper() == 'POST':
        post_url = urljoin(url, endpoint)   #join sources url with endpoint to create query path
        #find <input> -> <name>, store (name: value) to data
        input_name_todata(form, data)
        #find <select> -> <option> -> show bgp summary        
        select_option_todata(form, data)
        #call send post request function send_pst_req()
        return_text = send_pst_req([post_url, data])
        
#   if it's a get method
    elif method.upper() == 'GET':
        get_url = urljoin(url, endpoint)+'?'
        #find <select> -> <option> -> show bgp summary        
        select_option_todata(form, data)        
        #find <input> -> <name>, store (name: value) to data
        input_name_todata(form, data)
        #add all info in data to the source url to form a new request url
        for item in data:
            get_url += item +'='+ urllib.parse.quote_plus(data[item]) +'&'
        #call send get request function send_get_req()    
        return_text = send_get_req(get_url)
    
    return return_text
    

    
if __name__ == "__main__":
    url = 'http://lg.zsttk.ru/'
    resp = send_request(url)
