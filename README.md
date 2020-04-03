# BProp
An algorithm developed as a scientific research at Fluminense Federal University (UFF) to detect and prevent cycles in an incremental directed graph.The paper will be linked here as soon as it's released.<br/>
It uses Networkx (https://networkx.github.io/) and tqdm (https://tqdm.github.io/) to keep track of the progress on large graphs.

The strong point on this algorithm is the ability to know how to get from one node to another without exploring the graph with search algorithms like DFS and BFS. The other strong point is that it's possible to check if an edge will form a cycle with a single comparison with complexity O(n/log n). To ensure that, every node must know all of their ancestors/antecessors (nodes that can reach them), not just their immediate neighbors. Every node has a binary number assigned to them, starting from 1, and the ancestors is represented as an integer with the sum of the number of each node they can reach. As for checking whether there is a cycle, when inserting an (x, y) edge we just need to do a binary comparison to know if y is an ancestor of x.

The code for Bernstein and Chechik's (https://www.semanticscholar.org/paper/Incremental-Topological-Sort-and-Cycle-Detection-in-Bernstein-Chechik/1df7af6b7dd1bc67d9f35f2fdd0a2e97087ab7e1) was adapted from https://github.com/Sun-Jc/CycleDetectionOnDirectedGraph
