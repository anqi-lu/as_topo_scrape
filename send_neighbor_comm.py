import requests
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib
import os
import datetime
import html5lib
import time
import validators

'''send post request, return html text results, need further data ectraction'''
def send_pst_req(url_data):
    try:
        r = requests.post(url = url_data[0], data = url_data[1], timeout=10) 
    except:
        raise ValueError('request error')
    
    return r.text

'''send get request, return html text results, need further data ectraction'''
def send_get_req(url):
    try:
        r = requests.get(url, timeout=10)
    except:
        raise ValueError('request error')
    
    return r.text

'''get text for a tag'''
def bs4_get_string(nxt_el):
    if type(nxt_el) == bs4.element.NavigableString:
        nxt_el_str = nxt_el.strip()
    elif type(nxt_el) == bs4.element.Tag:
        nxt_el_str = nxt_el.text.strip()
    else:
        raise ValueError("form tag not exist")
    return nxt_el_str
    
'''loop through all input tags, find needed arguments for data'''
def inputs_process(inputs, data):
    for inp in inputs:
        if 'name' in inp.attrs:
            key = inp.attrs['name']
            if 'type' not in inp.attrs:
                if key not in data:
                    data[key]=[]
                    data[key].append(['','cust_arg'])
                continue

            if inp.attrs['type'].lower() == 'text':
                if key not in data:
                    data[key]=[]
                data[key].append(['','cust_arg'])
                continue
            
            if 'value' in inp.attrs:
                value = inp.attrs['value']
            elif 'type' in inp.attrs:
                if inp.attrs['type'].lower() == 'submit':
                    value = 'Submit'
                elif inp.attrs['type'].lower() == 'text':
                    value = ''
                elif inp.attrs['type'].lower() == 'reset':
                    value = ''
                else:
                    raise ValueError("type not as submit or text")
            else:
                raise ValueError("no value and type in input tag")
                
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
            
'''loop through all input tags, find needed arguments for data'''
def select_process(selects, data):
    for select in selects:
        if 'name' not in select.attrs:
            continue
        key = select.attrs['name']
        options = select.find_all('option')
        for option in options:
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
            if 'value' not in option.attrs:
                value = text
            else:
                value = option.attrs['value'] 
            if key not in data:
                data[key]=[]
            data[key].append([value, text])

'''only extract data with bgp summary'''            
def data_postprocess(data):
    post_data = {}
    sum_flag = False
    for key in data:
        attrs = data[key]
        if len(attrs) == 1:
            post_data[key] = attrs[0][0]
        else:
            is_bgp = False
#            post_data[key] = attrs[0][0]
            for attr in attrs:
                text = attr[1]
                if 'bgp' in text.lower() and 'sum' in text.lower(): #BGP summary
                    sum_flag = True
                    is_bgp = True
                    if key in post_data:
                        post_data[key].append(attr[0])
                    else:
                        post_data[key] = [attr[0]]
                    break
            if not is_bgp:
                post_data[key] = data[key]
    if not sum_flag:
        raise ValueError("bgp summary not found")
    return post_data

                
'''input AS source url, return html text'''
def gen_request(final_url, method, post_data, fold):
    file_name = final_url
#    print(final_url, method, post_data)
    #if it's a post method
    if method.upper() == 'POST':
           #join sources url with endpoint to create query path
        return_text = send_pst_req([final_url, post_data])
    #if it's a get method
    elif method.upper() == 'GET':
        final_url = final_url+'?'
        #add all info in data to the source url to form a new request url   
        for item in post_data:
            final_url = final_url + item +'='+ urllib.parse.quote_plus(post_data[item]) +'&'
        #call send get request function send_get_req()
        return_text = send_get_req(final_url)
        
    '''the ASN only contained in pre tag'''    
    response = BeautifulSoup(return_text, 'html5lib')
    pres = response.find_all('pre')
    if len(pres) > 0:
        dest = 'data/output/results/'+fold+'/pre'
        text = pres[0].text
        valid_out = True
    else:
        dest = 'data/output/results/'+fold+'/nopre'
        text = return_text
        valid_out = False
    if len(fold)>0:
        if not os.path.exists(dest):
            os.makedirs(dest)
        file_path = os.path.join(dest, ''.join(e for e in file_name if e.isalnum())+'_'+str(datetime.datetime.now()).replace(':','')+'.txt')
        with open(file_path, 'a') as f:
            f.write(file_name+'\n')
            f.write(str(post_data)+'\n')
            f.write(text)
    return text, valid_out

def find_neighbor_ip(text, ips4, ips6):
    for line in text.splitlines():
        words = line.strip().split()
        if len(words) > 0:
            if validators.ip_address.ipv4(words[0]): 
                ips4.append(words[0])
            if validators.ip_address.ipv6(words[0]):
                ips6.append(words[0])
    
def walk_data(data, method, url, ips4, ips6, add_ip, dest=''):
    data_process = data.copy()
    min_tree = True
    for key in data:
        attrs = data[key]
        if type(attrs) == list:
            if len(attrs) > 1:
                min_tree = False
                for attr in attrs:
                    data_process[key] = attr[0]
                    walk_data(data_process, method, url, ips4, ips6, add_ip, dest)
            else:
                data_process[key] = attrs[0][0]
    
    if min_tree:
        time.sleep(5)
        try:
            text, valid_out = gen_request(url, method, data_process, dest)
            if valid_out and add_ip:
                find_neighbor_ip(text, ips4, ips6)
        except ValueError as err:
            print(err.args)
    
                
def send_request(url, mode='sum'):
        #get form contents inside the html
    r = requests.get(url)
    while r.url != url:
        url = r.url
        r = requests.get(url)
    html = r.content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'html5lib')
    '''all the needed info is inside the [form] frame
    if html donesn't contain form tag, raise error'''
    forms = soup.find_all('form')
    if len(forms) == 0:
        raise ValueError("form tag not exist")
    form = forms[0]

    selects = form.find_all('select')
    inputs = form.find_all('input')
    
    '''determine method (GET or POST)'''
    if 'method' in form.attrs:
        method = form.attrs['method']
    else:
        method = 'GET'
        
    if 'action' in form.attrs:    
        endpoint = form.attrs['action']
    else:
        endpoint = ''
    
    final_url = urljoin(url, endpoint)
    
    data = {}
    
    inputs_process(inputs, data)
    select_process(selects, data)
    
#    post_data = data_postprocess(data)
    sum_comm = {}
    neibv4_comm = {}
    neibv6_comm = {}
    query_key = []
    for key in data:
        entries = data[key]
        for entry in entries:
            value, text = entry[0].lower(), entry[1].lower()
            if ('sum' in text) and ('bgp' in text):
                if key not in query_key:
                    query_key.append(key)
                if key not in sum_comm:
                    sum_comm[key] = []
                sum_comm[key].append([value, text])
                
    if len(query_key) > 1:
        raise ValueError("More than 1 query key found")
    
    neibv4_comm[query_key[0]] = []
    neibv6_comm[query_key[0]] = []
    for entry in data[query_key[0]]:
        value, text = entry[0].lower(), entry[1].lower()
        if ('advertised' in text) or ('received' in text) or ('neighbor' in text):
            if '6' in text:
                neibv6_comm[query_key[0]].append([value, text])
            else:
                neibv4_comm[query_key[0]].append([value, text])
        
    for key in data:
        if len(data[key]) == 1 and data[key][0][1] == 'cust_arg':
            arg_key = key
    
    if len(sum_comm[query_key[0]]) > 0:
        data.pop(query_key[0], None)
        data.update(sum_comm)
        ips4 = []
        ips6 = []
        walk_data(data, method, final_url, ips4, ips6, True, 'summ')
        
    if len(neibv4_comm[query_key[0]])>0 and len(ips4) >0:  
        ip_dict = {arg_key:[]} 
        data.pop(query_key[0], None)
        data.pop(arg_key, None)
        for ip in ips4:
            ip_dict[arg_key].append([ip, 'cust_arg'])
        data.update(ip_dict)
        data.update(neibv4_comm)
        walk_data(data, method, final_url, ips4, ips6, False, 'neighbor4')
        
    if len(neibv6_comm[query_key[0]])>0 and len(ips6) >0:  
        ip_dict = {arg_key:[]} 
        data.pop(query_key[0], None)
        data.pop(arg_key, None)
        for ip in ips6:
            ip_dict[arg_key].append([ip, 'cust_arg'])
        data.update(ip_dict)
        data.update(neibv6_comm)
        walk_data(data, method, final_url,ips4, ips6, False, 'neighbor6')
        
                
    
    

    
if __name__ == "__main__":
    url = 'https://www.lonap.net/cgi-bin/mrlg.cgi'
    resp = send_request(url)
