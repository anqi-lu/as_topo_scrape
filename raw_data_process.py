import os, shutil
from pathlib import Path
import numpy as np
from asnutils import host2asn
from urllib.parse import urlparse
import json
import re

asn_lookup = {}

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def summ_data_process():
    pathlist = Path('pre').glob('*.txt*')
    cnter=0
    valid_url = {}
    all_url = {}
    for i, p in enumerate(pathlist):
        f=str(p)
        valid_input = False
        neighbors = []
        borrow_num = 0
        with open(f, 'r') as file:
            lines = file.readlines()


            for line in lines[2:]:
                line = line.strip().lower()
                line_s = line.split()

                if valid_input:

                    if len(line_s)>0:
                        if len(line_s) < as_location+1:
                            borrow_num = len(line_s)
                        else:
                            neighbor = line_s[as_location - borrow_num].replace('as', '')
                            if neighbor == '4' or neighbor == '6' or 'ipv' in neighbor:
                                neighbor = line_s[as_location - borrow_num + 1].replace('as', '')
                            borrow_num = 0
                            if neighbor == '0':
                                continue
                            try:
                                neighbors.append(str(int(neighbor)))
                            except:
                                continue


                if len(line_s) >= 2:
                    if line_s[0] == 'neighbor' or line_s[0] == 'peer' or line_s[0] == 'ip':
                        if 'asn' in line_s:
                            as_location=line_s.index('asn')
                        elif 'as' in line_s:
                            as_location=line_s.index('as')
                        elif 'as#' in line_s:
                            as_location=line_s.index('as#')
                        else:
#                            shutil.copy(f, 'trash_bin/'+f[4:])
#                            raise ValueError(f)
                            continue

                        if 'address' in line_s:
                            if line_s.index('address') == 1:
                                as_location -= 1

                        valid_input = True
                        cnter+=1

            url = urlparse(lines[0]).hostname
            all_url[url]=1
            if valid_input:
                if url not in valid_url:
                    valid_url[url]=1
                if url not in asn_lookup:
                    asn = host2asn(url)
                    asn_lookup[url] = asn
                else:
                    asn = asn_lookup[url]
                data_dict = {}
                data_dict['asn'] = str(asn)
                data_dict['neighbors'] = []
                for neib in neighbors:
                    data_dict['neighbors'].append({'asn':neib})
                filename = str(cnter)+'.json'
                with open('LG_data/'+filename, 'w') as fp:
                    json.dump(data_dict, fp)

            else:
                shutil.copy(f, 'trash_bin/'+f[4:])

def nei_data_process():
    pathlist = Path('data/output/results/neighbor6/pre').glob('*.txt*')
    bgp_pairs = {}
    for i, p in enumerate(pathlist):
        if i%100 == 0:
            print(i)
        f=str(p)
        valid_input = False
        start_index = 0
        with open(f, 'r') as file:
            lines = file.readlines()
            url = urlparse(lines[0]).hostname
            asn_get = False
            while not asn_get:
                try:
                    asn = host2asn(url)
                    asn_get = True
                except:
                    print(url, 'get asn failed')
            
            for line in lines[2:]:
                line = line.strip('\n').lower()

                if valid_input:
                    if ' ' not in line:
                        continue
                    cand_index = [m.start() for m in re.finditer(' ', line[:start_index])]
                    words = line[cand_index[-1]:].split()
                    if len(words) > 1:
                        neighbors = []
                        for word in words:
                            if isInt(word):
                                if word == '0':
                                    neighbors == []
                                else:
                                    if len(neighbors) > 0:
                                        if neighbors[-1] != word:
                                            neighbors.append(word)
                                    else:
                                        neighbors.append(word)
                            elif word == 'i':
                                neighbors.append(str(asn))
                        if len(neighbors) > 1:
                            for i in range(len(neighbors)-1):
                                a, b = neighbors[i:i+2]
                                if int(a) > int(b):
                                    bgp_pairs[b+','+a] = 1
                                else:
                                    bgp_pairs[a+','+b] = 1
                                
                else:
                    if 'next' in line and 'hop' in line and 'path' in line:
                        valid_input = True
                        start_index = line.find('path')
    return bgp_pairs

def save_bgp_pairs(bgp_pairs):
    with open('neighbor_links.txt', 'a') as f:
        for key in bgp_pairs:
            f.write(key+'\n')
    

if __name__ == "__main__":
    bgp_pairs = nei_data_process()
    save_bgp_pairs(bgp_pairs)
    

