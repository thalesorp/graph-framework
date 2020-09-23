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

class AdjacencyListGraph:

    ''' A graph abstract data type using adjacency list representation'''

    def __init__(self, directed, wheighted, vertex_quantity=None):
        ''' "directed" and "wheight" MUST be boolean. '''

        self.undirected = not directed
        self.wheighted = wheighted
        self.vertex_quantity = None

        if vertex_quantity is not None:
            self.set_vertex_quantity(vertex_quantity)

    # CRUD
    def set_vertex_quantity(self, vertex_quantity):
        ''' Set the quantity of vertices and define the structure for their edges.'''

        self.vertex_quantity = vertex_quantity

        if self.wheighted:
            self.edges = [dict() for _ in range(self.vertex_quantity)]
        else:
            self.edges = [list() for _ in range(self.vertex_quantity)]

    def insert_edge(self, origin, destination, wheight=None):
        ''' Inserts an edge from vertex origin to vertex destination.'''

        if self.wheighted:
            self.edges[origin][destination] = wheight

            if self.undirected:
                self.edges[destination][origin] = wheight

        else:
            self.edges[origin].append(destination)

            if self.undirected:
                self.edges[destination].append(origin)

    def remove_edge(self, origin, destination):
        ''' Removes an edge from vertex u to vertex v.'''

        if self.wheighted:
            del self.edges[origin][destination]

            if self.undirected:
                del self.edges[destination][origin]

        else:
            self.edges[origin].remove(destination)

            if self.undirected:
                self.edges[destination].remove(origin)

    def has_edge(self, origin, destination):
        ''' Checks if there's a edge from vertex origin to vertex destination.'''

        if destination in self.edges[origin]:
            return True
        return False

    def delete(self):
        foo = True

    # Utils
    def show_graph(self):
        ''' Prints the whole structure.'''

        for i in range(len(self.edges)):
            print(i, end=" = ")
            if self.wheighted:
                print(self.edges[i], end =" ")
            else:
                for adjacency in self.edges[i]:
                    print(adjacency, end =" ")
            print()

    def graph_from_file(self, file_path):
        ''' Receives a file path and read it as follows:
        "VERTEX_QUANTITY
        EDGE_QUANTITY"
        This meaning that, the two first lines is the vertices quantity and edge quantity,
        respectively. After that, it contains EDGE_QUANTITY lines as follows:
        "ORIGIN DESTINATION WHEIGHT"'''

        graph_file = open(file_path,'r')

        self.set_vertex_quantity(int(graph_file.readline()))
        edge_quantity = int(graph_file.readline())

        for line in graph_file:
            origin, destination, wheight = line.split()
            self.insert_edge(int(origin), int(destination), float(wheight))

        graph_file.close()

    # Useful algorithms
    def depth_first_search_util(self, vertex, visited):
        # Marking the current vertex as visited
        visited[vertex] = True
        print(vertex, end = ' ')

        for i in range(len(self.edges)):
            if visited[i] is False:
                self.depth_first_search_util(i, visited)

    def depth_first_search(self, vertex):
        # Marking all vertices as not visited
        #visited = [False] * self.vertex_quantity
        visited = [[False] for _ in range(self.vertex_quantity)]

        self.depth_first_search_util(vertex, visited)











class AdjacencyMatrixGraph:

    ''' A graph abstract data type using adjacency matrix representation'''

    def __init__(self, n_vertices, directed):

        self.vertex_quantity = int(n_vertices)
        self.undirected = not directed

        self.m = [[0 for _ in range(self.vertex_quantity)] for _ in range(self.vertex_quantity)]
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
