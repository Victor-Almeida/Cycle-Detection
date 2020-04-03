import networkx as nx
from tqdm import tqdm
import time

class BPGraph(nx.DiGraph):           
    def __init__(self):
        super().__init__()
        self.next_index = 0
        self.binary_predecessors = []
        self.binary_successors = []
        self.neighbors = []
    
    def neighbors(self, index):
        return list(self[index])
    
    def __propagate(self, index_to, visited = 0):        
        visited = visited | 1 << index_to
        if(self.binary_successors[index_to] > 0):
            for successor in self.__get_indexes(self.binary_successors[index_to]): 
                self.binary_predecessors[successor] = self.binary_predecessors[successor] | self.binary_predecessors[index_to]
                
            for successor in self.__get_indexes(self.binary_successors[index_to]): 
                if 1 << successor & visited != 0:
                    self.__propagate(successor, visited)
            
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
        self.binary_predecessors.append(0)
        self.binary_successors.append(0)
        self.neighbors.append(0)
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
            if(not self.add_edge(edge[0], edge[1])):
                cycles.append(edge)
            pbar.update(1)
        pbar.close()
        return cycles
        
    def add_edge(self, node_from, node_to, decrement = False):        
        if(node_from == node_to):     # if it's a reflexive edge, then it's a cycle
            return False
        
        if decrement:
            index_from = node_from -1   # if the nodes start from 1 instead of 0, we must decrement them
            index_to = node_to - 1
        else:
            index_from = node_from
            index_to = node_to

        
        if(self.binary_predecessors[index_from] & (1 << index_to) or # if the target edge is an predecessorof the origin
          self.binary_predecessors[index_from] & self.binary_successors[index_to]):  # if the target edge has a successor that is an predecessorof the starting edge
            return False
        else:        
            self.binary_predecessors[index_to] = self.binary_predecessors[index_to] | self.binary_predecessors[index_from] | (1 << index_from)
            self.neighbors[index_from] = self.neighbors[index_from] | (1 << index_to)
            self.__propagate(index_to)
            super().add_edge(index_from, index_to)            
            return True
        
######################### DFS #############################################

    def classic_dfs(self, start, target, visited):
        cycle = False
        for next_edge in list(self[start]):
            if next_edge == target:
                return True
            elif next_edge not in visited:
                visited.append(next_edge)
                cycle = self.classic_dfs(next_edge, target, visited)
                if cycle:
                    return True
                else:
                    visited.pop()  
                    if visited == []:
                        return False
        return False
    
    def incremental_dfs(self, edges):
        cycles = []
        pbar = tqdm(total = len(edges))
        
        for edge in edges:
            if not self.add_dfs_edge(edge[0], edge[1]):
                cycles.append(edge)
            pbar.update(1)
        pbar.close()
        return cycles
            
    def add_dfs_edge(self, node_from, node_to):
        if node_from == node_to:
            return False
        elif self.classic_dfs(node_to, node_from, [node_to]):
            return False
        else:
            super().add_edge(node_from, node_to)
            return True    
        
######################### BFS #############################################

    def classic_bfs(self, start, target, visited):
        cycle = False
        for next_edge in list(self[start]):
            if next_edge == target:
                return True
            
        for next_edge in list(self[start]):
            if next_edge not in visited:
                visited.append(next_edge)
                cycle = self.classic_bfs(next_edge, target, visited)
                if cycle:
                    return True
                else:
                    visited.pop()
                    if visited == []:
                        return False
            
        return False
    
    def incremental_bfs(self, edges):
        cycles = []
        pbar = tqdm(total = len(edges))
        
        for edge in edges:
            if not self.add_bfs_edge(edge[0], edge[1]):
                cycles.append(edge)
            pbar.update(1)
        pbar.close()
        return cycles
            
    def add_bfs_edge(self, node_from, node_to):
        if node_from == node_to:
            return False
        elif self.classic_bfs(node_to, node_from, [node_to]):
            return False
        else:
            super().add_edge(node_from, node_to)
            return True    