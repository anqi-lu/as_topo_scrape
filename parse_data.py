import csv
import re
import ipaddress
import json
from pathlib import Path
from topo_graph import TopoNode

DET_LINE_NUMBER = 4

"""
takes in a filename in string,
find the neigbor table 
make a json object 
write into a json file
"""
def parse(filename):
    node_json = {}
    node_json['ip'] = ""
    node_json['asn'] = ""
    node_json['neighbors'] = []

    with open(filename, 'r') as f:
        data = f.readlines()
    
    # print(data[:6])
    flag = 0
    last_num_tokens = 0
    as_col_number = 2 # default the third column

    own_ip = ""
    own_as = ""
    neighbor_node_json = []

    for i, line in enumerate(data):
        # can add more characters that we dont need
        line = line.replace(',', '')
        line = line.replace('\n', '')
        
        tokens = line.split()

        if "local as number" in line.lower():
            try:
                own_as = line.split("number", 1)[1]
            except:
                print("cannot find as number in file: " + filename)
                
            # let's hope both ip and asn are in the same line
            print(line)
            for token in tokens:
                
                if match_ips(token) is not None:
                    own_ip = token

        # print(tokens)
        last_num_tokens = len(tokens)

        if len(tokens) == last_num_tokens:
            flag += 1
        # determine it's a table when 4 lines have the same number of tokens 
        # and the first of the token is an ip address 
        if not tokens:
            continue
        if flag >= DET_LINE_NUMBER and match_ips(tokens[0]) is not None: # table found
            headerline = data[i - 1]
            for k, header in enumerate(headerline.split()):
                if "as" in header.lower():
                    # the column number is the as column number
                    as_col_number = k

            if as_col_number >= len(tokens):
                # AS col doesn't match the current row 
                return None 

            # make neighbor topo nodes 
            neighbor_node_json.append({'ip': tokens[0], 'asn':tokens[as_col_number]})

    if len(own_ip) > 0 and len(own_as) > 0:
        node_json['ip'] = own_ip
        node_json['asn'] = own_as
        node_json['neighbors'] = neighbor_node_json
        write_node(node_json)

    return None

"""  """
def parse_files(directory_in_str):
    pathlist = Path(directory_in_str).glob('*.txt')
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)
        parse(path_in_str)

# helper functions

""" parse out valid ip addresses """
def match_ips(s):
    try:
        return ipaddress.ip_address(s)
    except:
        return None 

def write_node(node_json):
    ip = node_json['ip']
    asn = node_json['asn']
    name = ip + '_' + asn
    with open('data/nodes/' + name + '.json', 'w') as outfile:
        json.dump(node_json, outfile, indent=2)

def main():
    lg_summary = 'data/output/summary/'
    lg_neighbor = 'data/output/neighbor/'
    parse_files(lg_summary)
    #node_json = parse(lg_summary+ 'as-ielo.net.lg.txt')

if __name__ == "__main__":
    main()