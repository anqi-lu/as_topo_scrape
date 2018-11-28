import csv
import re
import ipaddress
import json
from pathlib import Path

DET_LINE_NUMBER = 4
AS_KEYWORDS = set(["as", "As", "AS", "ASN", "as#", "AS#", "asn"])

"""
takes in a filename in string,
find the neigbor table 
make a json object 
write into a json file
"""
def parse(filename, subdir):
    node_json = {}
    node_json['ip'] = ""
    node_json['asn'] = ""
    node_json['neighbors'] = []

    with open(filename, 'r') as f:
        data = f.readlines()

    flag = 0
    last_num_tokens = 0

    own_ip = ""
    own_as = ""
    current_asn = ""
    current_ip = 

    neighbor_node_json = []
    AS_NUM_SPECIFIED = False

    for i, line in enumerate(data):
        # can add more characters that we dont need
        line = line.replace(',', '')
        line = line.replace('\n', '')
        line = line.lower()
        
        tokens = line.split()

        if "local as number" in line:
            try:
                own_as = line.split("number", 1)[1]
                AS_NUM_SPECIFIED = True
            except:
                pass 
                # gonna assume own AS number is the first line 
                
            # let's hope both ip and asn are in the same line
            print(line)
            for token in tokens:
                if match_ip(token) is not None:
                    own_ip = token

        last_num_tokens = len(tokens)

        if len(tokens) == last_num_tokens:
            flag += 1
        # determine it's a table when 4 lines have the same number of tokens 
        # and the first of the token is an ip address 
        if not tokens:
            continue
        if flag >= DET_LINE_NUMBER and match_ip(tokens[0]) is not None: # table found

            for token in tokens:
                if match_ip(token):
                    current_ip = token
                if is_string_valid_asn(token):
                    current_asn = token

            if not AS_NUM_SPECIFIED:
                # assume the first row is its own as number and ip
                own_as = current_asn
                own_ip = current_ip
                AS_NUM_SPECIFIED = True
            else:
                # make neighbor topo nodes 
                neighbor_node_json.append({'ip': current_ip, 'asn':current_asn})

    if len(own_ip) > 0 and len(own_as) > 0:
        node_json['ip'] = own_ip
        node_json['asn'] = own_as
        node_json['neighbors'] = neighbor_node_json
        write_node(node_json, subdir)

    return None

# helper functions

""" parse out valid ip addresses """
def match_ip(s):
    try:
        return ipaddress.ip_address(s)
    except:
        return None 

""" determine whether a column value is an ASN """
def is_string_valid_asn(s):
    # 2 byte: 1 to 65535
    # 4 byte: 1.0 to 65535.65535
    if s.isdigit():
        return is_number_valid_asn(s)
    else:
        if "." in s:
            nums = s.split(".")
            if len(nums) != 2:
                return False 
            
            return is_number_valid_asn(nums[0]) and is_number_valid_asn(nums[1])

def is_number_valid_asn(s):
    if s.isdigit():
        if int(s) >= 1 and int(s) <= 65535:
            return True 

""" write a node into a json file """
def write_node(node_json, subdir):
    ip = node_json['ip']
    asn = node_json['asn']
    name = ip + '_' + asn
    with open('data/nodes/' + subdir + '/' + name + '.json', 'w') as outfile:
        json.dump(node_json, outfile, indent=2)

""" walk through the text files (data from LG servers) and parse each one """
def parse_files(directory_in_str):
    pathlist = Path(directory_in_str).glob('*.txt')
    subdir = directory_in_str.split('/')[-1]
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)
        parse(path_in_str, subdir)

def main():
    lg_summary = 'data/output/summary/'
    lg_neighbor = 'data/output/neighbor/'
    lg_database = 'data/output/database/'
    lg_failed_neighbor = 'have asn but failed to read/BGP neighbor'
    lg_failed_sum = 'have asn but failed to read/BGP sum'
    lg_failed_newdataset= 'have asn but failed to read/new dataset'
    #parse_files(lg_summary)
    parse_files(lg_failed_neighbor)
    parse_files(lg_failed_sum)
    parse_files(lg_failed_newdataset)

if __name__ == "__main__":
    main()