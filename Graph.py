#! python3
#!/usr/bin/env python3

################################################################################
#                                                                              #
#  Graph framework                                                             #
#                                                                              #
#  Thales Otávio | @ThalesORP | ThalesORP@gmail.com                            #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2020                    #
#                                                                              #
################################################################################

''' This module contains two graph abstract data type: adjacency list and adjacency matrix'''

import sys
from operator import itemgetter

LOWERCASE_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
LETTERS = "l"
NUMBERS = "n"

class AdjacencyListGraph:

    ''' A graph abstract data type using adjacency list representation'''

    def __init__(self, directed, weighted, vertex_naming_convention, vertex_quantity=None):
        ''' "directed" and "weight" MUST be boolean.
        "vertex_naming_convention" cvan be "l" for lowercase letters, or "n" for numbers.'''

        self.undirected = not directed
        self.weighted = weighted
        self.vertex_quantity = None

        self.edges = dict()

        if self.weighted:
            self.weights = dict()

        self.vertex_naming_convention = vertex_naming_convention.lower()

        if vertex_quantity is not None:
            self.set_vertex_quantity(vertex_quantity)

    # CRUD
    def set_vertex_quantity(self, vertex_quantity):
        ''' Set the quantity of vertices and define the structure for their edges.'''

        self.vertex_quantity = vertex_quantity

        for i in range(vertex_quantity):
            if self.vertex_naming_convention == LETTERS:
                vertex_name = LOWERCASE_ALPHABET[i]

            if self.vertex_naming_convention == NUMBERS:
                vertex_name = i

            self.edges[vertex_name] = []

            if self.weighted:
                self.weights[vertex_name] = []

    def insert_edge(self, origin, destination, weight=None):
        ''' Inserts an edge from vertex origin to vertex destination.'''

        self.edges[origin].append(destination)
        if self.weighted:
            self.weights[origin].append(weight)

    def has_edge(self, origin, destination):
        ''' Checks if there's a edge from vertex origin to vertex destination.'''

        if (origin in self.edges) and (destination in self.edges[origin]):
            return True
        return False

    def __str__(self):
        ''' Returns a string with the whole structure ready to be printed.'''

        result = "{\n"

        for vertex_origin in self.edges:
            result += "  " + str(vertex_origin) + " = "

            for i in range(len(self.edges[vertex_origin])):
                result += str(self.edges[vertex_origin][i])
                if self.weighted:
                    result += ":" + str(self.weights[vertex_origin][i])
                result += " "

            result += "\n"

        result += "}"

        return result

    # Utils
    def get_adjacent_vertices(self, vertex):
        ''' Return a list containing all adjacent vertices of "vertex".'''

        adjacent_vertices = self.edges[vertex]

        for origin_vertex, destination_vertex_list in self.edges.items():
            if vertex in destination_vertex_list:
                adjacent_vertices.append(origin_vertex)

        return adjacent_vertices

    # Useful algorithms
    def depth_first_search(self, visited, vertex):
        ''' Depth first search algorithm.'''

        # Marking the current vertex as visited
        visited[vertex] = True

        print(vertex, end=",")

        adjacent_vertices = self.get_adjacent_vertices(vertex)

        for adjacent_vertex in adjacent_vertices:
            if visited[adjacent_vertex] is False:
                self.depth_first_search(visited, adjacent_vertex)

    def connected_components(self):
        ''' Count how many connected components there is.'''

        connected_components_quantity = 0

        # Creating a dictionary with "False" as value for each vertex (which is used as key)
        visited = {key: False for key in self.edges.keys()}

        for origin_vertex in self.edges.keys():

            if visited[origin_vertex] is False:
                self.depth_first_search(visited, origin_vertex)
                connected_components_quantity += 1
                print()

        print(connected_components_quantity, "connected components", end="\n")

    def get_vertex_minimum_cost(self, costs, mst):
        ''' Prim's algorithm auxiliar function: returns the vertex name with minimum cost.'''

        minimum_value = sys.maxsize

        for vertex in self.edges.keys():
            if self.vertex_naming_convention == LETTERS:
                vertex = LOWERCASE_ALPHABET.index(vertex)

            if costs[vertex] < minimum_value and vertex not in mst:
                minimum_value = costs[vertex]
                elegible_vertex = vertex

        return elegible_vertex

    def minimum_spanning_tree(self):
        ''' Prim's algorithm.'''

        '''
        Q: Vértices que ainda não fazem parte da AGM parcial
        (ainda não fazem parte do conjunto X);

        chave[u]: peso da aresta mais leve do vértice u que a conecta à AGM
        parcialmente construída;

        π[u]: vértice pai do vértice u;
        '''

        inf = sys.maxsize

        mst = list()
        mst_cost = 0

        costs = [inf] * self.vertex_quantity
        costs[0] = 0

        for i in range(self.vertex_quantity):
            #print("\nInter:", i)

            vertex_minimum_cost = self.get_vertex_minimum_cost(costs, mst)
            #print("vertex_minimum_cost:", vertex_minimum_cost)

            #mst.append([vertex_minimum_cost, costs[vertex_minimum_cost]])

            #print("vertex_minimum_cost:", vertex_minimum_cost)
            mst.append(vertex_minimum_cost)
            mst_cost += costs[vertex_minimum_cost]

            destinations = self.edges[vertex_minimum_cost]
            destinations_costs = self.weights[vertex_minimum_cost]

            # Updating the costs list with the costs of the vertices connected
            # to the vertex with minimum cost picked.
            for i in range(len(destinations)):
                if costs[destinations[i]] > destinations_costs[i]:
                    costs[destinations[i]] = destinations_costs[i]

        return(mst_cost)



# URI problems
def uri_2426():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2426
    Input:
    "N" number of tests
    "V E" number of vertices and edges
    "O D" repeated E times, which each is a connection between two edges: origin and destination
    '''

    number_of_tests = input()

    for i in range(int(number_of_tests)):

        vertex_quantity, edge_quantity = input().split()

        directed = True
        weighted = False
        graph = AdjacencyListGraph(directed, weighted, int(vertex_quantity))

        for _ in range(int(edge_quantity)):
            origin, destination = input().split()
            graph.insert_edge(origin, destination)

        print("Case #" + str(i+1) + ":")
        graph.connected_components()

def uri_1081(): # Ok.
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1082
    Input:
    "N" number of tests
    "V E" number of vertices and edges
    "O D" repeated E times, which each is a connection between two edges: origin and destination
    '''

    number_of_tests = input()

    for i in range(int(number_of_tests)):

        vertex_quantity, edge_quantity = input().split()

        directed = True
        weighted = False
        vertex_naming_convention = "l"
        graph = AdjacencyListGraph(directed, weighted, vertex_naming_convention, int(vertex_quantity))

        for _ in range(int(edge_quantity)):
            origin, destination = input().split()
            graph.insert_edge(origin, destination)

        print("Case #" + str(i+1) + ":")
        graph.connected_components()

def uri_1774():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1774
    Input:
    "V E" number of vertices and edges
    "O D W" repeated E times, which each is a connection between two edges
    (origin and destination) and their weights.
    '''

    print("URI 1774")

    vertex_quantity, edge_quantity = input().split()

    directed = False
    weighted = True
    #graph = AdjacencyListGraph(directed, weighted, int(vertex_quantity))
    graph = AdjacencyMatrixGraph(directed, weighted, int(vertex_quantity))

    for _ in range(int(edge_quantity)):
        origin, destination, weight = input().split()
        graph.insert_edge(origin, destination, weight)

    graph.connected_components()

def uri_2127():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2127
    Input:
    "V E" number of vertices and edges
    "O D W" repeated E times, which each is a connection between two edges (origin and destination) and their weights.
    '''
    print("URI 2127")

    input_str = input()
    while input_str != "\n":

        vertex_quantity, edge_quantity = input_str.split()

        directed = False
        weighted = True
        graph = AdjacencyListGraph(directed, weighted, int(vertex_quantity))

        for _ in range(int(edge_quantity)):
            origin, destination, weight = input().split()
            #graph.insert_edge(origin, destination, weight)

        input_str = input()

        # Call solving algorithm here

def uri_2485():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2485'''
    return

def uri_1152(): # Ok.
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1152'''
    print("URI 1152")

    vertex_quantity, edge_quantity = input().split()

    while (vertex_quantity != "0") and (edge_quantity != "0"):

        directed = False
        weighted = True
        vertex_naming_convention = "n"
        graph = AdjacencyListGraph(directed, weighted, vertex_naming_convention, int(vertex_quantity))

        for _ in range(int(edge_quantity)):
            origin, destination, weight = input().split()
            graph.insert_edge(int(origin), int(destination), int(weight))

        vertex_quantity, edge_quantity = input().split()

        # Call solving algorithm here
        print(graph.minimum_spanning_tree())

# DEBUG
def debug():

    print("DEBUGGING...")

    directed = False
    weighted = True
    vertex_quantity = 9
    vertex_naming_convention = "n"
    g = AdjacencyListGraph(directed, weighted, vertex_naming_convention, vertex_quantity)

    g.insert_edge(0, 1, 4)
    g.insert_edge(0, 7, 8)

    g.insert_edge(1, 2, 8)
    g.insert_edge(1, 7, 11)

    g.insert_edge(2, 3, 7)
    g.insert_edge(2, 5, 4)
    g.insert_edge(2, 8, 2)

    g.insert_edge(3, 4, 9)
    g.insert_edge(3, 5, 14)

    g.insert_edge(4, 5, 10)

    g.insert_edge(5, 6, 2)

    g.insert_edge(6, 7, 1)
    g.insert_edge(6, 8, 6)

    g.insert_edge(7, 8, 7)

    g.minimum_spanning_tree()

#uri_2426()
#uri_1081() # Ok.
#uri_1774()
#uri_2127()
#uri_2485()
#uri_1152() #Ok.
#debug()
