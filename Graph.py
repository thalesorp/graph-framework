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

from sys import stdin

LOWERCASE_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class AdjacencyListGraph:

    ''' A graph abstract data type using adjacency list representation'''

    # TODO: delete this "self.vertices = list()" and use this "self.edges.keys()" OR BETTER, THIS "for key in dictionary" for more info, read this: https://github.com/Ericsson/codechecker/issues/2084 

    def __init__(self, directed, weighted, first_vertex, vertex_quantity=None):
        ''' "directed" and "weight" MUST be boolean.
        "first_vertex" can be "a" for lowercase letters,
        "0" or for numbers starting from zero, and "1" for start counting from one.'''

        self.undirected = not directed
        self.weighted = weighted
        self.first_vertex = first_vertex
        self.vertex_quantity = vertex_quantity

        self.edges = dict()

        if self.weighted:
            self.weights = dict()

        if vertex_quantity is not None:
            self.set_vertex_quantity()

    # CRUD
    def set_vertex_quantity(self):
        ''' Set the quantity of vertices and define the structure for their edges.'''

        for i in range(self.vertex_quantity):
            if self.first_vertex == "a":
                vertex_name = LOWERCASE_ALPHABET[i]
            elif self.first_vertex == "1":
                vertex_name = str(i + 1)
            else:
                vertex_name = str(i)

            self.edges[vertex_name] = list()

            if self.weighted:
                self.weights[vertex_name] = list()

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

        if origin in self.edges:
            if destination in self.edges[origin]:
                return True
        return False

    def __str__(self):
        ''' Returns a string with the whole structure ready to be printed. For debug purposes.'''

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

    # Utils and useful algorithms
    def get_adjacent_vertices(self, vertex):
        ''' Return a list containing all adjacent vertices of "vertex".'''

        return list(self.edges[vertex])

    def get_adjacent_vertices_with_weights(self, vertex):
        ''' Return two lists: one containing all adjacent vertices of "vertex",
        and another with their respectives weights.'''

        return list(self.edges[vertex]), list(self.weights[vertex])

    def depth_first_search(self, visited, vertex):
        ''' Depth first search algorithm.'''

        result = [vertex]

        # Marking the current vertex as visited
        visited[vertex] = True

        adjacent_vertices = self.get_adjacent_vertices(vertex)

        for adjacent_vertex in adjacent_vertices:
            if visited[adjacent_vertex] is False:
                result += self.depth_first_search(visited, adjacent_vertex)

        if result is not None:
            result.sort()
        return result

    def connected_components(self):
        ''' Count how many connected components there is.'''

        result_str = ""

        connected_components_quantity = 0

        # Creating a dictionary with "False" as value for each vertex (which is used as key)
        visited = {key: False for key in self.edges.keys()}

        for origin_vertex in self.edges.keys():

            if visited[origin_vertex] is False:
                result_str += str(self.depth_first_search(visited, origin_vertex)) + "\n"
                connected_components_quantity += 1

        # Formatting the output
        result_str = result_str.replace("[", "")
        result_str = result_str.replace("]", ",")
        result_str = result_str.replace("'", "")
        result_str = result_str.replace(" ", "")
        result_str += str(connected_components_quantity) + " connected components\n"
        return result_str

    def get_vertex_minimum_cost(self, vertices_costs, included_vertices):
        ''' Prim's algorithm auxiliar function: returns the vertex name with minimum cost.'''

        minimum_value = float("inf")

        for vertex in self.edges:
            if (vertices_costs[vertex] < minimum_value) and (included_vertices[vertex] is False):
                minimum_value = vertices_costs[vertex]
                elegible_vertex = vertex

        return elegible_vertex

    def minimum_spanning_tree(self):
        ''' Prim's algorithm.'''

        # List used to pick edge of minimum weight
        vertices_costs = dict()
        for vertex in self.edges:
            vertices_costs[vertex] = float("inf")
        # Making the first vertex costs 0 so that it get picked first
        vertices_costs[self.first_vertex] = 0

        # List to store the origin vertices of the MST solution
        origin_vertices = dict()
        for vertex in self.edges:
            origin_vertices[vertex] = None
        origin_vertices[self.first_vertex] = -1

        # Dictionary used to check if a vertex was included or not in the MST solution
        included_vertices = dict()
        for vertex in self.edges:
            included_vertices[vertex] = False

        # List used to store the origin, destination and weight of the MST solution
        mst_costs = list()

        for _ in range(self.vertex_quantity):

            vertex_minimum_cost = self.get_vertex_minimum_cost(vertices_costs, included_vertices)

            # Marking that this vertex was already picked
            included_vertices[vertex_minimum_cost] = True

            # Getting the adjacent vertices (and their weights) of the vertex with minimum cost
            adjacent_vertices, adjacent_vertices_weights = self.get_adjacent_vertices_with_weights(vertex_minimum_cost)

            # Iterating over the adjacent vertices and updating costs to go there
            for vertex, vertex_cost in zip(adjacent_vertices, adjacent_vertices_weights):
                if (included_vertices[vertex] is False) and (vertices_costs[vertex] > vertex_cost):
                    vertices_costs[vertex] = vertex_cost
                    origin_vertices[vertex] = vertex_minimum_cost

            mst_costs.append([vertex_minimum_cost, origin_vertices[vertex_minimum_cost], vertices_costs[vertex_minimum_cost]])

        '''
        print("ORIGIN\tDEST.\tWEIGHT")
        for i in range(1, len(mst_costs)):
            print(mst_costs[i][0], "\t", mst_costs[i][1], "\t", mst_costs[i][2])
        '''

        # Adding all the costs of MST to get the total cost.
        mst_total_cost = sum([row[2] for row in mst_costs])

        return mst_total_cost

    def breadth_first_search(self, starting_vertex, final_vertex):
        ''' Breadth first search algorithm. "vertex" is the starting point.'''

        elapsed_time = 0

        # Dictionary of colors. White: not discovered, gray: border, black: discovered
        color = {key: "white" for key in self.edges}
        color[starting_vertex] = "gray"

        # Dictionary used to store the depth of each vertex
        distance = {key: float("inf") for key in self.edges}
        distance[starting_vertex] = 0

        # Dictionary used to store the parent of each vertex
        parent = {key: None for key in self.edges}

        # Puting the source vertex on the list of current vertices to explore
        auxiliar_vertices = [starting_vertex]

        #print("auxiliar_vertices:", auxiliar_vertices, "\n")

        # While there is gray vertex in the auxiliar list, visit them and update their data.
        while auxiliar_vertices:
            print("\nAuxiliar vertices:", auxiliar_vertices)
            first_vertex = auxiliar_vertices.pop(0)
            #print("first_vertex:", first_vertex)
            adjacent_vertices, adjacent_vertices_weights = self.get_adjacent_vertices_with_weights(first_vertex)
            print("adjacent_vertices:", adjacent_vertices)
            #print("adjacent_vertices_weights:", adjacent_vertices_weights)

            # Going through all adjacent vertices of the first vertex in auxiliar list
            # and updating their respective data on color, distance and parent dictionaries.
            for vertex, vertex_cost in zip(adjacent_vertices, adjacent_vertices_weights):

                if color[vertex] == "white":
                    # Only taking the paths with "weight = 1"
                    weight_equals_one = (elapsed_time % 3 == 0) and (vertex_cost == 1)
                    #print("weight_equals_one:", weight_equals_one)
                    # Only taking the paths with "weight = 0"
                    weight_equals_zero = (elapsed_time % 3 != 0) and (vertex_cost == 0)
                    #print("weight_equals_zero:", weight_equals_zero)

                    if weight_equals_one or weight_equals_zero:
                        color[vertex] = "gray"
                        distance[vertex] = distance[first_vertex] + 1
                        parent[vertex] = first_vertex
                        auxiliar_vertices.append(vertex)


            # Marking the first vertex of auxiliar vertices as black, which means that
            # his already discovered.
            color[first_vertex] = "black"
            if first_vertex == final_vertex:
                pass
            print("BLACK VERTICES:", first_vertex)
            elapsed_time += 1


            '''print("color:", color)
            print("distance:", distance)
            print("parent:", parent)'''

        print("\n")
        print("elapsed_time:", elapsed_time)
        print("auxiliar_vertices:", auxiliar_vertices)
        print("color:", color)
        print("distance:", distance)
        print("parent:", parent)


        '''
        path = [final_vertex]
        vertex = final_vertex
        while parent[vertex] is not None:
            path.insert(0, parent[vertex])
            vertex = parent[vertex]
        '''
        path = list()
        for vertex in self.edges:
            path = [vertex]
            while parent[vertex] is not None:
                path.insert(0, parent[vertex])
                vertex = parent[vertex]
            print("path:", path)

        if parent[final_vertex] is None:
            #print("There is no way to reach the way out.")
            print("*")
        else:
            print("The way out is this path:", path)

        return distance, parent

    def bomb(self, entry, way_out):
        ''' '''

        elapsed_time = 0
        current_vertex = entry
        path = [current_vertex]

        while current_vertex != way_out:

            adjacent_vertices, adjacent_vertices_weights = self.get_adjacent_vertices_with_weights(entry)

            for vertex, vertex_cost in zip(adjacent_vertices, adjacent_vertices_weights):

                # Only taking the paths with "weight = 1"
                weight_equals_one = (elapsed_time % 3 == 0) and (vertex_cost == 1)
                # Only taking the paths with "weight = 0"
                weight_equals_zero = (elapsed_time % 3 != 0) and (vertex_cost == 0)

                if weight_equals_one or weight_equals_zero:
                    current_vertex = vertex
                    elapsed_time += 1
                    path.append(current_vertex)
                    break


        print("path:", path)


        '''

        # Now trying to follow that path.

        current_vertex = path[0]
        next_vertex = path[1]

        for i in range(len(path)):
            current_vertex = path[0]
            next_vertex = path[1]
            if elapsed_time % 3 == 0:
                # Take only the routes with weight = 1
                if self.weights[current_vertex][next_vertex] != 1:
                    return "*"
            else:
                # Take only the routes with weight = 0
                if self.weights[current_vertex][next_vertex] != 0:
                    return "*"
            elapsed_time += 1
    
        '''

################################################################################
#                                                                              #
# URI problems                                                                 #
#                                                                              #
################################################################################

def uri_2426():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2426'''

    #vertex_quantity, entry, way_out, edge_quantity = input().split()]
    vertex_quantity = 6
    entry = "5"
    way_out = "4"

    directed = True
    weighted = True
    first_vertex = "0"
    graph = AdjacencyListGraph(directed, weighted, first_vertex, int(vertex_quantity))

    graph.insert_edge("0", "1", 0)
    graph.insert_edge("1", "2", 0)
    graph.insert_edge("1", "2", 1)
    graph.insert_edge("2", "3", 1)
    graph.insert_edge("2", "4", 0)
    graph.insert_edge("3", "0", 0)
    graph.insert_edge("5", "0", 1)

    print(graph.bomb(entry, way_out))
    #distance, parent = graph.breadth_first_search(entry, way_out)

def uri_1082():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1082'''

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
        print(graph.connected_components())

def uri_1774():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/1774'''

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

def uri_2127():
    '''https://www.urionlinejudge.com.br/judge/en/problems/view/2127'''

    instance = 0

    input_str = input()
    while input_str != "":

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

def uri_1152():
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

#uri_2426()
#uri_1082() # Ok
#uri_1774() # Ok
#uri_2127() # Correct answers but getting "Runtime error". Outputs of uDebug matches. https://www.udebug.com/URI/2127
uri_1152() # Correct answers, but getting "Time limit exceeded".  Outputs of uDebug matches. https://www.udebug.com/URI/1152
