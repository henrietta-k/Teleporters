"""
Teleporters

Incoming Dean of the College, Melina Hale, has decided that winters have gotten too long and by next winter, the beloved tunnels connecting the entire campus should be accessible once again. Unfortunately, all the old tunnels running under the quad have become unusable and new ones need to be built. Of course, this should be kept economical and financially responsible. An engineering firm has provided all possible tunnels that could be dug, and of course the price tag for each of them. In a wild revelation, Fermilab announced that they now have a working teleporter, but it only works for short distances. The engineering firm has provided estimates for installing these teleporters in various building around campus (but not all). The dean wants all buildings to be connected by at least one path, but also for the entire project to cost as low as possible. To that end, you need to find the best set of tunnels and (maybe) teleporters to connect the entire campus for the next winter.

Input: In the first line there are three integers $N$, $K$, $M$, which correspond to the number of buildings, the number of buildings where a teleporter can be installed and the number of possible tunnels between buildings.
In the next $K$ lines there are two integers, $i$ and $B[i]$, meaning that a teleporter can be installed in building $i$ with cost $B[i]$.
Finally, the next $M$ lines contain three integers $i$, $j$, $c[i, j]$, which denote that there is a proposed tunnel between buildings $i$ and $j$ with cost $c[i, j]$.

Output: One line with a single integer, the minimum cost for the entire network.
"""

from queue import PriorityQueue

class Node:
    """
    Class for a Node object representing a building

    Attributes:
        name(int): the building's number
        parent(int): the parent Node in the MST
        rank(int): the Node's rank in the MST

    """
    def __init__(self, name, rank):
        self.name = name
        self.parent = self
        self.rank = rank


def solve(N, teleporters, edges):
    """
    Solves the problem by running Kruskal's once without teleporters and once
    with teleporters then finding the minimum of the two results

    Inputs:
        N(int): the total number of buildings
        teleporters(lst of ints): where teleporters can be installed and the
            cost of installing the teleporter
        edges(lst of ints): two buildings and the length of a possible tunnel
            between them

    Returns(int): the min cost of the entire network with both teleporters and
        tunnels
    """

    #Running Kruskal's without the teleporters
    tunnels_result = kruskals(N, edges)

    #Connecting all teleporters to a fake Node
    inv_node = N + 1
    for teleporter in teleporters:
        building, cost = teleporter
        edges.append([building, inv_node, cost])

    #Running Kruskal's on the graph with teleporters
    teleporters_result = kruskals(inv_node, edges)

    return min(tunnels_result, teleporters_result)


def kruskals(vertices, edges):
    """
    Runs Kruskal's on the set of vertices and edges to find the Minimum
    Spanning Tree

    Inputs:
        vertices(lst of ints): all buildings
        edges(lst of lst of ints): edges between buildings

    Returns(int): the min cost of the network
    """
    sets = {}
    for vertex in range(1, vertices + 1):
        sets[vertex] = Node(vertex, 0)

    result = 0
    queue = PriorityQueue()
    for edge in edges:
        queue.put((edge[2], edge))

    num_edges = 0

    #Using union-find to create the MST
    while num_edges < vertices - 1:
        build_1, build_2, cost = queue.get()[1]
        if find(sets, build_1) != find(sets, build_2):
            result += cost
            num_edges += 1
            union(sets, build_1, build_2)

    return result


def find(sets, vertex):
    """
    Find the set that the building belongs in

    Inputs:
        sets(dict): keeps track of all sets
        vertex(int): the building to find the set for

    Returns(int): the set that the vertex belongs to
    """
    if sets[vertex].parent.name == vertex:
        return vertex
    parent = sets[vertex].parent.name
    child = vertex
    while parent != child:
        child = parent
        parent = sets[child].parent.name
    return parent


def union(sets, build_1, build_2):
    """
    Joins the two disjoint sets that build_1 and build_2 belong in

    Inputs:
        sets(dict): all sets
        build_1(int): the first building
        build_2(int): the second building
    """
    parent_1 = find(sets, build_1)
    parent_2 = find(sets, build_2)

    if parent_1 == parent_2:
        return

    building_1 = sets[parent_1]
    building_2 = sets[parent_2]
    if building_1.rank > building_2.rank:
        building_2.parent = building_1
    else:
        building_1.parent = building_2
        if building_1.rank == building_2.rank:
            building_2.rank += 1


def read_input():
    """
    Reading the input from a .txt file
    """
    N, K, M = [int(i) for i in input().split()]
    teleporters = [[int(i) for i in input().split()] for _ in range(K)]
    edges = [[int(i) for i in input().split()] for _ in range(M)]
    return N, K, M, teleporters, edges


def main():
    N, _, _, teleporters, edges = read_input()
    cost = solve(N, teleporters, edges)
    print(cost)


if __name__ == '__main__':
    main()