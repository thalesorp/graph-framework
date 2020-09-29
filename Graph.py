#! python3
#!/usr/bin/env python3

################################################################################
#                                                                              #
#  Graph framework                                                             #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Thales Otávio | @ThalesORP | ThalesORP@gmail.com                            #
#                                                                              #
#  Date: 2020                                                                  #
#                                                                              #
################################################################################

''' This module contains two graph abstract data type: adjacency list and adjacency matrix'''

LOWERCASE_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class AdjacencyListGraph:

    ''' A graph abstract data type using adjacency list representation'''

    def __init__(self, directed, weighted, vertex_quantity=None):
        ''' "directed" and "wheight" MUST be boolean. '''

        self.undirected = not directed
        self.weighted = weighted
        self.vertex_quantity = None

        self.edges = dict()

        if self.weighted:
            self.weights = dict()

        if vertex_quantity is not None:
            self.set_vertex_quantity(vertex_quantity)

    # CRUD
    def set_vertex_quantity(self, vertex_quantity):
        ''' Set the quantity of vertices and define the structure for their edges.'''

        self.vertex_quantity = vertex_quantity

        for i in range(vertex_quantity):
            self.edges[LOWERCASE_ALPHABET[i]] = []

    def insert_edge(self, origin, destination, wheight=None):
        ''' Inserts an edge from vertex origin to vertex destination.'''

        self.edges[origin].append(destination)
        if self.weighted:
            self.weights[origin].append(wheight)

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

# URI problems
def uri_1081():
    ''' URI 1082: https://www.urionlinejudge.com.br/judge/en/problems/view/1082
    Input:
    "N" number of tests
    "V E" number of vertices and edges
    "O D" lines, each is a connection between two edges: origin and destination
    '''

    number_of_tests = input()

    for i in range(int(number_of_tests)):

        vertex_quantity, edge_quantity = input().split()

        directed = True
        wheighted = False
        graph = AdjacencyListGraph(directed, wheighted, int(vertex_quantity))

        for _ in range(int(edge_quantity)):
            origin, destination = input().split()
            graph.insert_edge(origin, destination)

        print("Case #" + str(i+1) + ":")
        graph.connected_components()

def uri_1774():
    ''' URI 1774: https://www.urionlinejudge.com.br/judge/en/problems/view/1774
    '''
    print("URI 1774")

# DEBUG
def debug():

    print("DEBUGGING...")

    directed = True
    wheighted = True
    g = AdjacencyListGraph(directed, wheighted)

    g.insert_edge("a", "b", 21)
    g.insert_edge("a", "c", 35)
    g.insert_edge("b", "c", 23)

    print(g.has_edge("a", "c"))
    print(g.has_edge("b", "c"))

    print(g)

uri_1081()
uri_1774()
