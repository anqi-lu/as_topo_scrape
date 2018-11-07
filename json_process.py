import json, os
from pathlib import Path
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pickle
import matplotlib as mpl

class Tree:
    def __init__(self):
        self.nodes = {}
        self.degrees = []
        self.links = {}
        
    def load_data(self, data_path):
        tree = pickle.load(open(data_path, "rb"))
        self.nodes = tree.nodes
        
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
                    
    def add_all_data(self, save_path):
        pathlist = Path(save_path).glob('*.json')
        for p in pathlist:
            f=str(p)
            json_file = open(f)
            json_str = json_file.read()
            json_data = json.loads(json_str)
            self.add_data(json_data)
                    
    def gen_degree_map(self):
        for node in self.nodes:
            if len(self.nodes[node]) < 5000:
                degree = len(self.nodes[node])
            else:
                degree = 5000
            self.degrees.append(degree)
            
    def num_nodes(self):
        asns = {}
        for key in self.nodes:
            node = self.nodes[key]
            if key not in asns:
                asns[key] = key
            for neighbor in node:
                if neighbor not in asns:
                    asns[neighbor] = neighbor
        
        return asns
    
    def add_links(self):
        for node in self.nodes:
            neibs = self.nodes[node]
            for neib in neibs:
                if int(node) >= int(neib):
                    link = str(neib)+'_'+str(node)
                else:
                    link = str(node) + '_' + str(neib)
                self.links[link] = 1
                
    def extra_links(self, tree):
        self.links = {}
        tree.links = {}
        self.add_links()
        tree.add_links()
        not_in_links = []
        for link in tree.links:
            if link not in self.links:
                not_in_links.append(link)
        return not_in_links
        
    def extra_nodes(self, tree):
        this_nodes = self.num_nodes()
        other_nodes = tree.num_nodes()
        not_in_nodes = []
        for node in other_nodes:
            if node not in this_nodes:
                not_in_nodes.append(node)
        return not_in_nodes
        
def fix_hist_step_vertical_line_at_end(ax):
    axpolygons = [poly for poly in ax.get_children() if isinstance(poly, mpl.patches.Polygon)]
    for poly in axpolygons:
        poly.set_xy(poly.get_xy()[1:])            

if __name__ == "__main__":
#    tree = Tree()
#    pathlist = Path('LG_data').glob('*.json')
#    for p in pathlist:
#        f=str(p)
#        json_file = open(f)
#        json_str = json_file.read()
#        json_data = json.loads(json_str)
#        tree.add_data(json_data)
#    pickle.dump(tree, open("LG.data", "wb"))
    
    tree0 = Tree()
    tree1 = Tree()
    tree2 = Tree()
    tree3 = Tree()
    tree0.load_data("irl.data")
    tree1.load_data("LG.data")
    tree2.load_data("irl_2013.data")
    tree3.load_data("LG_2013.data")
    fig, ax = plt.subplots(figsize=(8, 4))
    tree0.gen_degree_map()
    tree1.gen_degree_map()
    tree2.gen_degree_map()
    tree3.gen_degree_map()
    x0 = tree0.degrees
    x1 = tree1.degrees
    x2 = tree2.degrees
    x3 = tree3.degrees
    ax.hist(x0, bins='auto', range=None, density=1, histtype='step', cumulative=-1, log = True, label='IRL_latest')
    ax.hist(x2, bins='auto', range=None, density=1, histtype='step', cumulative=-1, log = True, label='IRL_2013')
    ax.hist(x1, bins='auto', range=None, density=1, histtype='step', cumulative=-1, log = True, label='LG_latest')
    ax.hist(x3, bins='auto', range=None, density=1, histtype='step', cumulative=-1, log = True, label='LG_2013')
    fix_hist_step_vertical_line_at_end(ax)
    ax.legend(loc='right')
    ax.set_xlabel('degree')
    ax.set_ylabel('CCDF')
    
    plt.show()
    

