# Cycle Detection
An algorithm developed as a scientific research at Fluminense Federal University (UFF) to detect and prevent cycles in an incremental directed graph. (The paper will be linked here as soon as it's released)
It uses Networkx (https://networkx.github.io/) and tqdm (https://tqdm.github.io/) to keep track of the progress on large graphs.

The strong point on this algorithm is the ability to know how to get from one node to another without exploring the graph with search algorithms like DFS and BFS. The other strong point is that it's possible to check if an edge will form a cycle with a single comparison with complexity O(1). To ensure that, every node must know all of their ancestrals (nodes that can reach them) and successors (nodes they can reach), not just their immediate neighbors. Every node has a binary number assigned to them, starting from 1, and the ancestrals and successors' sets are represented as an integer with the sum of the number of each node they can reach. As for checking whether there is a cycle, we just need to do a binary comparison to know if they have each other as an ancestral/successor.
