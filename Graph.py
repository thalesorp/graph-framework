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

    def __init__(self, directed, weighted, first_vertex, vertex_quantity=None):
        ''' "directed" and "weight" MUST be boolean.
        "first_vertex" can be "a" for lowercase letters,
        "0" or for numbers starting from zero, and "1" for start counting from one.'''

        self.undirected = not directed
        self.weighted = weighted
        self.vertex_quantity = None
        self.first_vertex = first_vertex

        self.edges = dict()

        self.vertices = list()

        if self.weighted:
            self.weights = dict()

        if vertex_quantity is not None:
            self.set_vertex_quantity(vertex_quantity)

    # CRUD
    def set_vertex_quantity(self, vertex_quantity):
        ''' Set the quantity of vertices and define the structure for their edges.'''

        self.vertex_quantity = vertex_quantity

        for i in range(vertex_quantity):
            if self.first_vertex == "a":
                vertex_name = LOWERCASE_ALPHABET[i]
            elif self.first_vertex == "1":
                vertex_name = str(i + 1)
            else:
                vertex_name = str(i)

            self.edges[vertex_name] = []

            if self.weighted:
                self.weights[vertex_name] = []

            self.vertices.append(vertex_name)

    def insert_edge(self, origin, destination, weight=None):
        ''' Inserts an edge from vertex origin to vertex destination.'''

        self.edges[origin].append(destination)
        if self.weighted:
            self.weights[origin].append(weight)

        if self.undirected:
            self.edges[destination].append(origin)
            if self.weighted:
                self.weights[destination].append(weight)

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

        adjacent_vertices = list(self.edges[vertex])
        return adjacent_vertices

    def get_adjacent_vertices_with_weights(self, vertex):
        ''' Return two lists: one containing all adjacent vertices of "vertex",
        and another with their respectives weights.'''

        adjacent_vertices = list(self.edges[vertex])
        adjacent_vertices_weights = list(self.weights[vertex])
        return adjacent_vertices, adjacent_vertices_weights

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

    def get_vertex_minimum_cost(self, vertices_costs, included_vertices):
        ''' Prim's algorithm auxiliar function: returns the vertex name with minimum cost.'''

        minimum_value = float("inf")

        for vertex in self.vertices:
            if (vertices_costs[vertex] < minimum_value) and (included_vertices[vertex] is False):
                minimum_value = vertices_costs[vertex]
                elegible_vertex = vertex

        return elegible_vertex

    def minimum_spanning_tree(self):
        ''' Prim's algorithm.'''

        # List used to pick edge of minimum weight
        vertices_costs = dict()
        for vertex in self.vertices:
            vertices_costs[vertex] = float("inf")
        # Making the first vertex costs 0 so that it get picked first
        vertices_costs[self.first_vertex] = 0

        # List to store the origin vertices of the MST solution
        origin_vertices = dict()
        for vertex in self.vertices:
            origin_vertices[vertex] = None
        origin_vertices[self.first_vertex] = -1

        # Dictionary used to check if a vertex was included or not in the MST solution
        included_vertices = dict()
        for vertex in self.vertices:
            included_vertices[vertex] = False

        # List used to store the origin, destination and weight of the MST solution
        mst_costs = list()


        for _ in range(self.vertex_quantity):

            vertex_minimum_cost = self.get_vertex_minimum_cost(vertices_costs, included_vertices)

            # Marking that this vertex was already picked
            included_vertices[vertex_minimum_cost] = True

            # Getting the adjacent vertices (and their weights) of the vertex with minimum cost
            adjacence_vertices, adjacence_vertices_weights = self.get_adjacent_vertices_with_weights(vertex_minimum_cost)

            # Iterating over the adjacent vertices and updating costs to go there
            for vertex, vertex_cost in zip(adjacence_vertices, adjacence_vertices_weights):
                if (included_vertices[vertex] is False) and (vertices_costs[vertex] > vertex_cost):
                    vertices_costs[vertex] = vertex_cost
                    origin_vertices[vertex] = vertex_minimum_cost

            mst_costs.append([vertex_minimum_cost, origin_vertices[vertex_minimum_cost], vertices_costs[vertex_minimum_cost]])

        '''
        print("ORIGIN\tDEST.\tWEIGHT")
        for i in range(1, len(mst_costs)):
            print(mst_costs[i][0], "\t", mst_costs[i][1], "\t", mst_costs[i][2])
        '''

        # Getting the total cost of the MST.
        mst_total_cost = sum([row[2] for row in mst_costs])

        return(mst_total_cost)













# URI problems
def uri_2426():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2426
    Input:
    "N" number of tests
    "V E" number of vertices and edges
    "O D" repeated E times, which each is a connection between two edges: origin and destination
    '''

    print("URI 2426")

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

def uri_1082(): # Ok
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1082
    Input:
    "N" number of tests
    "V E" number of vertices and edges
    "O D" repeated E times, which each is a connection between two edges: origin and destination
    '''

    number_of_tests = input()

    for i in range(int(number_of_tests)):

        vertex_quantity, edge_quantity = input().split()

        directed = False
        weighted = False
        first_vertex = "a"
        graph = AdjacencyListGraph(directed, weighted, first_vertex, int(vertex_quantity))

        for _ in range(int(edge_quantity)):
            origin, destination = input().split()
            graph.insert_edge(origin, destination)

        print("Case #" + str(i+1) + ":")
        graph.connected_components()

def uri_1774(): # Ok
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1774
    Input:
    "V E" number of vertices and edges
    "O D W" repeated E times, which each is a connection between two edges
    (origin and destination) and their weights.
    '''

    vertex_quantity, edge_quantity = input().split()

    directed = False
    weighted = True
    first_vertex = "1"
    graph = AdjacencyListGraph(directed, weighted, first_vertex, int(vertex_quantity))

    for _ in range(int(edge_quantity)):
        origin, destination, weight = input().split()
        graph.insert_edge(origin, destination, int(weight))

    print(graph.minimum_spanning_tree())

    '''
    DEBUG
    print("URI 1774")

    vertex_quantity = 7
    edge_quantity = 12

    directed = False
    weighted = True
    first_vertex = "1"
    graph = AdjacencyListGraph(directed, weighted, first_vertex, int(vertex_quantity))

    graph.insert_edge("1", "3", 6)
    graph.insert_edge("1", "4", 9)
    graph.insert_edge("2", "3", 17)
    graph.insert_edge("2", "5", 32)
    graph.insert_edge("2", "7", 27)
    graph.insert_edge("3", "4", 11)
    graph.insert_edge("3", "5", 4)
    graph.insert_edge("4", "5", 3)
    graph.insert_edge("4", "6", 19)
    graph.insert_edge("5", "6", 13)
    graph.insert_edge("5", "7", 15)
    graph.insert_edge("6", "7", 5)

    print(graph.minimum_spanning_tree())
    '''

def uri_2127(): # Ok, but "Runtime error"
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2127
    Input:
    "V E" number of vertices and edges
    "O D W" repeated E times, which each is a connection between two edges (origin and destination) and their weights.
    '''

    instance = 0

    input_str = input()
    while input_str is not "":

        vertex_quantity, edge_quantity = input_str.split()

        directed = False
        weighted = True
        first_vertex = "1"
        graph = AdjacencyListGraph(directed, weighted, first_vertex, int(vertex_quantity))

        for _ in range(int(edge_quantity)):
            origin, destination, weight = input().split()
            graph.insert_edge(origin, destination, int(weight))

        instance += 1
        print("Instancia", instance)
        print(graph.minimum_spanning_tree())
        print()

        input_str = input()

def uri_2485():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2485'''

    print("URI 2485")

    return

def uri_1152(): # Ok, but "Time limit exceeded"
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1152'''

    vertex_quantity, edge_quantity = input().split()

    while (vertex_quantity != "0") and (edge_quantity != "0"):

        directed = False
        weighted = True
        first_vertex = "0"
        graph = AdjacencyListGraph(directed, weighted, first_vertex, int(vertex_quantity))

        total_cost = 0

        for _ in range(int(edge_quantity)):
            origin, destination, weight = input().split()
            graph.insert_edge(origin, destination, int(weight))
            total_cost += int(weight)

        vertex_quantity, edge_quantity = input().split()

        print(total_cost - graph.minimum_spanning_tree())

# DEBUG
def debug():

    #print("DEBUGGING...")

    #uri_2426()
    #uri_1082() # Ok, but "Wrong answer (100%)"
    #uri_1774() # Ok
    uri_2127() # Ok, but "Runtime error"
    #uri_2485()
    #uri_1152()  # Ok, but "Time limit exceeded"

debug()
