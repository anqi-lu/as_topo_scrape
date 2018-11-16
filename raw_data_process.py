import os, shutil
from pathlib import Path
import numpy as np
from asnutils import host2asn
from urllib.parse import urlparse
import json

asn_lookup = {}

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
                
if __name__ == "__main__":
    pathlist = Path('data/output/neighbor').glob('*.txt*')
    cnter=0
    valid_url = {}
    all_url = {}
    for i, p in enumerate(pathlist):
        f=str(p)
        print(f)
                    
            
