import json, os
from pathlib import Path
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class Tree:
    def __init__(self):
        self.nodes = {}
        self.degrees = []
        
    def add_data(self, data):
        asn = data['asn'].strip()
        neighbors=[]
        for n in data['neighbors']:
            if n['asn'] != asn:
                neighbors.append(n['asn'].strip())
                
        if asn not in self.nodes:
            self.nodes[asn] = []
            for neighbor in neighbors:
                if neighbor not in self.nodes[asn]:
                    self.nodes[asn].append(neighbor)
        else:
            for neighbor in neighbors:
                if neighbor not in self.nodes[asn]:
                    self.nodes[asn].append(neighbor)
                    
    def gen_degree_map(self):
        for node in self.nodes:
            degree = len(self.nodes[node])
            self.degrees.append(degree)
            

if __name__ == "__main__":
    tree = Tree()
    pathlist = Path('data/nodes').glob('*.json')
    for p in pathlist:
        f=str(p)
        json_file = open(f)
        json_str = json_file.read()
        json_data = json.loads(json_str)
        tree.add_data(json_data)
        
    tree.gen_degree_map()
    de = tree.degrees
    plt.hist(de)