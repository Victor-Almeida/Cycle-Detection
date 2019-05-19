import random
import math
import sys
from tqdm import tqdm as tqdm_no_notebook
from tqdm import tqdm_notebook
import networkx as nx
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

class BPGraph(nx.DiGraph):           
    def __init__(self):
        super().__init__()
        self.next_index = 0
        self.binary_antecessors = []
        self.binary_successors = []
    
    def __propagate(self, index_to):        
        if(self.binary_successors[index_to] > 0):
            for successor in self.__get_indexes(self.binary_successors[index_to]): 
                if(successor > 0 and (successor & self.__get_number(index_to))):
                    self.binary_antecessors[successor] = self.binary_antecessors[successor] | self.binary_antecessors[index_to]
                    self.binary_successors[index_to] = self.binary_successors[index_to] | self.binary_successors[successor]
                    self.__propagate(successor)
            
    def __get_indexes(self, bin_sum):
        num = bin_sum
        powers = []
        counter = 0
        while num > 0:
            if(num % 2):
                powers.append(counter)
            num = num >> 1
            counter = counter + 1
        return powers
    
    def __get_number(self, index):
        number = 1
        for i in range(0, index):
            number = number << 2
        return number
    
    def add_node(self):
        super().add_node(self.next_index)
        self.next_index = self.next_index + 1
        self.binary_antecessors.append(0)
        self.binary_successors.append(0)
        return self.next_index
    
    def add_n_nodes(self, n):
        nodes = []
        for i in range(0, n):
            nodes.append(self.add_node())
        return nodes
    
    def add_incremental_edges(self, edges):
        cycles = []
        pbar = tqdm(total = len(edges))
        for edge in edges:
            if(not self.add_edge(edge[0] + 1, edge[1] + 1)):
                cycles.append(edge)
            pbar.update(1)
        pbar.close()
        return cycles
        
    def add_edge(self, node_from, node_to):        
        if(node_from == node_to):
            return False
                
        index_from = node_from - 1
        index_to = node_to - 1
        
        antecessors = self.binary_antecessors[index_from] | (1 << index_from)
        successors = self.binary_successors[index_to] | (1 << index_to)
        
        if(self.binary_antecessors[index_from] & (1 << index_to) or 
          self.binary_antecessors[index_to] & (1 << index_from)):
            return False
        else:        
            self.binary_antecessors[index_to] = antecessors
            if(self.binary_successors[index_to] > 0):
                self.__propagate(index_to)
            self.binary_successors[index_from] = successors
            super().add_edge(index_from, index_to)            
            return True
    
    def classic_dfs(self, start, visited):
      cycle = False
      for next_edge in list(self.neighbors(start)):
        if next_edge in visited:
          return True
        else:
          visited.append(next_edge)
          cycle = self.classic_dfs(next_edge, visited)
          if cycle:
            return True
      return False
    
    def incremental_dfs(self, edges):
      cycles = []
      pbar = tqdm(total = len(edges))
      for edge in edges:
        if edge[0] == edge[1]:
          cycles.append(edge)
        elif self.classic_dfs(edge[1], [edge[1], edge[0]]):
          cycles.append(edge)
        else:
          super().add_edge(edge[0], edge[1])
        pbar.update(1)
      pbar.close()
      return cycles
    
    def add_dfs_nodes(self, N):
      for i in range(N):
        super().add_node(i)
