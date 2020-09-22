#! python3
#!/usr/bin/env python3

################################################################################
#                                                                              #
#  Graph                                                                       #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Thales Otávio | @ThalesORP | ThalesORP@gmail.com                            #
#                                                                              #
#  Date: 2020                                                                  #
#                                                                              #
################################################################################

''' This module contains two graph abstract data type: adjacency list and adjacency matrix.'''

class AdjacencyListGraph:

    ''' A graph abstract data type using adjacency list.'''

    def __init__(self, n_vertices, directed):

        self.n_vertices = int(n_vertices)
        self.directed = directed
        self.undirected = not directed

        self.adjacency_list = [[] for _ in range(n_vertices)]

    def insert_edge(self, u, v):
        ''' Inserts an edge from vertex u to vertex v.'''

        self.adjacency_list[u].append(v)

    def remove_edge(self, u, v):
        ''' Removes an edge from vertex u to vertex v.'''

        self.adjacency_list[u].remove(v)

    def has_edge(self, u, v):
        ''' Checks if there's a edge from vertex u to vertex v.'''

        if v in self.adjacency_list[u]:
            return True
        return False

    def show_graph(self):
        ''' Prints the whole structure.'''

        for i in range(len(self.adjacency_list)):
            print(i, end=": ")
            for adjacency in self.adjacency_list[i]:
                print(adjacency, end =" ")
            print()

class AdjacencyMatrixGraph:

    ''' A graph abstract data type using adjacency matrix.'''

    def __init__(self, n_vertices, directed):

        self.n_vertices = int(n_vertices)
        self.directed = directed
        self.undirected = not directed

        self.m = [[0 for _ in range(self.n_vertices)] for _ in range(self.n_vertices)]
        print(self.m)

    def insert_edge(self, u, v):
        ''' Inserts an edge from vertex u to vertex v.'''

        self.m[u][v] = 1
        if self.undirected:
            self.m[v][u] = 1

    def remove_edge(self, u, v):
        ''' Removes an edge from vertex u to vertex v.'''

        self.m[u][v] = 0
        if self.undirected:
            self.m[v][u] = 0

    def has_edge(self, u, v):
        ''' Checks if there's a edge from vertex u to vertex v.'''

        if self.m[u][v] == 1:
            return True
        return False

    def show_graph(self):
        ''' Print the adjacency matrix.'''

        for row in self.m:
            for value in row:
                print(value, end =" ")
            print()
