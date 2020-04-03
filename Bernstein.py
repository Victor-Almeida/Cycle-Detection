import random
import math
import sys
from tqdm import tqdm as tqdm_no_notebook
from tqdm import tqdm_notebook
import networkx as nx
import time
import matplotlib.pyplot as plt

class Bernstein(nx.DiGraph):           
    def __init__(self):
        super().__init__()
        self.A = []
        self.D = []
        self.As = []
        self.Ds = []
        self.AA = []
        self.logs = []
        self.S = set()
        
    def backable_add(self, obj, element):
        if element not in obj:
            obj.add(element)
            self.logs.append((obj, element))

            
    def update(self, a,b):
        a_ancestors = [x for x in nx.ancestors(self, a)] + [a]
        b_descendants = [x for x in nx.descendants(self, b)] + [b]
        
        for s in b_descendants:
            if s in self.S:
                for anc in a_ancestors:
                    self.backable_add(self.A[s], anc)
                    self.backable_add(self.Ds[anc], s)
        for s in a_ancestors:
            if s in self.S:
                for des in b_descendants:
                    self.backable_add(self.D[s], des)
                    self.backable_add(self.As[des], s)

            
    def is_s_equivalent(self, u,v):
        return len(self.As[u]) == len(self.As[v]) and len(self.Ds[u]) == len(self.Ds[v])
            
        
    def check(self, a,b):
        to_explore = set([b])
        while len(to_explore) > 0:
            w = to_explore.pop()
            if w == a:
                return False
            if w in self.AA[a]:
                return False
            elif a in self.AA[w]:
                pass
            elif not self.is_s_equivalent(a, w):
                pass
            else:
                self.backable_add(self.AA[w], a)
                for w,z in self.out_edges(w):
                    to_explore.add(z)
        return True
    
    def add_n_nodes(self, N):
        self.add_nodes_from(list(range(N)))
        sample_prob_threshold = 11 * math.log(N) / math.sqrt(N)
        self.S = set([i for i in range(N) if random.random() <= sample_prob_threshold])

        self.A = [set([i]) for i in range(N)]
        self.D = [set([i]) for i in range(N)]
        self.As = [set([i]).intersection(self.S) for i in range(N)]
        self.Ds = [set([i]).intersection(self.S) for i in range(N)]

        self.AA = [set([i]) for i in range(N)]
        
    def add_edge(self, s, t):
        super().add_edge(s,t)
        self.update(s,t)
        if not self.check(s,t):
            #yield G, (s,t), id_node
            # rollback
            while len(self.logs) > 0:
                obj, element = self.logs.pop()
                obj.remove(element)
            self.remove_edge(s,t)
            return False
        else:
            return True