# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 21:57:59 2018

@author: genix
"""
import shutil


with open('read_failure.txt','r') as f:
    i = 0
    line_list = f.readlines()
    for line in line_list:
        with open(line.strip(), 'r') as fi:
            fi.readline()
            fi.readline()
            string = fi.read().lower()
            a = string.find('AS#')
            b = string.find('as#')
            c = string.find('as ')
            d = string.find(' as')
            e = string.find('error')
            if e >=0:
                continue
            elif a == -1 and b == -1 and c == -1 and d == -1:
                continue
            else:
                with open('read_failure_success_count.txt', 'a') as f:
                    f.write(line.strip()+'\n')
                    shutil.copy(line.strip(), 'success/'+str(i)+'.txt')
                    i = i + 1
    print(i)

#with open(r'data\output\results\pre\httpasielonetlg_2018-10-30 205809.322811.txt'.replace('\\','/'), 'r') as f:
#    a = f.readlines()