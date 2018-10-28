import requests
import bs4
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
#         find from <table> frame
#         table -> td - > input (name , value)
#         find all names with its value
#         store (name:value) to data, if a name with no value, then value = ''
# =============================================================================           
def table_input_todata(form, data):
    table = form.find_all('table')[0]
    for td in table.find_all('td'):
        text = td.text
        if 'bgp' in text and '6' not in text and 'sum' in text:
            inp = td.find_previous_sibling("td").find('input')
            if 'name' in inp.attrs:
                key = inp.attrs['name']
                if 'value' in inp.attrs:
                    val = inp.attrs['value']
                else:
                    val = ''
                data[key] = val
                break 
    for inp in table.find_all('input'):
        if 'type' in inp.attrs:
            if inp.attrs['type'].upper == 'TEXT':
                data[inp.attrs['name']] = inp.attrs['value']

#whether is a scroll type form
def is_scroll(form):
    if len(form.find_all('select')) == 0:
        return False
    return True

def bs4_get_string(nxt_el):
    if type(nxt_el) == bs4.element.NavigableString:
        nxt_el_str = nxt_el.strip()
    elif type(nxt_el) == bs4.element.Tag:
        nxt_el_str = nxt_el.text.strip()
    else:
        raise ValueError("form tag not exist")
    return nxt_el_str
    

def inputs_process(inputs, data):
    for inp in inputs:
        if 'name' in inp.attrs:
            key = inp.attrs['name']
            if 'type' not in inp.attrs:
                if key not in data:
                    data[key]=[]
                    data[key].append(['',''])
                continue

            if inp.attrs['type'].lower() == 'text':
                if key not in data:
                    data[key]=[]
                data[key].append(['',''])
                continue
            
            if 'value' in inp.attrs:
                value = inp.attrs['value']
            elif 'type' in inp.attrs:
                if inp.attrs['type'].lower() == 'submit':
                    value = 'Submit'
                elif inp.attrs['type'].lower() == 'text':
                    value = ''
                
            text = ''
            if inp.attrs['type'].lower() == 'radio':
                nxt_el = inp.next_element
                nxt_el_str = bs4_get_string(nxt_el)
                    
                while len(nxt_el_str) == 0:
                    nxt_el = nxt_el.next_element
                    if type(nxt_el) == bs4.element.Tag:
                        if nxt_el.name.lower() == 'input':
                            break
                    nxt_el_str = bs4_get_string(nxt_el)
                text = nxt_el_str
            if key not in data:
                data[key]=[]
            data[key].append([value, text])

def select_process(selects, data):
    for select in selects:
        key = select.attrs['name']
        options = select.find_all('option')
        for option in options:
            value = option.attrs['value']   
            text=''
            nxt_el = option.next_element
            nxt_el_str = bs4_get_string(nxt_el)
            while len(nxt_el_str) == 0:
                nxt_el = nxt_el.next_element
                if type(nxt_el) == bs4.element.Tag:
                    if nxt_el.name.lower() == 'option':
                        break
                nxt_el_str = bs4_get_string(nxt_el)
            text = nxt_el_str
            if key not in data:
                data[key]=[]
            data[key].append([value, text])
            
def data_postprocess(data):
    post_data = {}
    for key in data:
        attrs = data[key]
        if len(attrs) == 1:
            post_data[key] = attrs[0][0]
        else:
            post_data[key] = attrs[0][0]
            for attr in attrs:
                text = attr[1]
                if 'bgp' in text and '6' not in text and 'sum' in text: #BGP summary
                    post_data[key] = attr[0]
                    break
    return post_data
                
                
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
    html = r.content.decode('utf-8', 'ignore')
#    r_text = r.text
    soup = BeautifulSoup(html, 'html.parser')
    #all the needed info is inside the [form] frame
    forms = soup.find_all('form')
    if len(forms) == 0:
        raise ValueError("form tag not exist")
    form = forms[0]

    selects = form.find_all('select')
    inputs = form.find_all('input')
    
    
#    if not(len(selects) == 1 or len(tables) == 1):
#        raise ValueError("Form structure violation", len(selects), len(tables))
    
    #determine method (GET or POST)
    if 'method' in form.attrs:
        method = form.attrs['method']
    else:
        method = 'GET'
        
    if 'action' in form.attrs:    
        endpoint = form.attrs['action']
    else:
        endpoint = ''
        
    #create data lib to store request info
    data = {}
    
    inputs_process(inputs, data)
    select_process(selects, data)
    
    post_data = data_postprocess(data)

    #if it's a post method
    if method.upper() == 'POST':
        post_url = urljoin(url, endpoint)   #join sources url with endpoint to create query path
        return_text = send_pst_req([post_url, post_data])
#   if it's a get method
    elif method.upper() == 'GET':
        get_url = urljoin(url, endpoint)+'?'
        #add all info in data to the source url to form a new request url   
        for item in post_data:
            get_url = get_url + item +'='+ urllib.parse.quote_plus(post_data[item]) +'&'
        #call send get request function send_get_req()
        return_text = send_get_req(get_url)
        
    response = BeautifulSoup(return_text, 'html.parser')
    pres = response.find_all('pre')
    if len(pres) > 0:
        return pres[0].text
    else:
        return return_text
    

    
if __name__ == "__main__":
    url = 'https://lg.maxiweb.com.br/cgi-local/lg.cgi'
    resp = send_request(url)
