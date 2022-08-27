import random
import numpy as np

from algorithms_ALP.src.algorithms.ACO.data_structure.EdgeALP import EdgeALP


class GraphALP:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.edges = {}
        self.neighbors = {}

    def add_edge(self, origin, destination, cost):
        new_edge = EdgeALP(origin, destination, cost)
        self.edges[(origin, destination)] = new_edge

        if origin not in self.neighbors:
            self.neighbors[origin] = [destination]
        else:
            self.neighbors[origin].append(destination)

    def get_edge_cost(self, origin, destination):
        return self.edges[(origin, destination)].get_cost()

    def get_edge_pheromony(self, origin, destination):
        return self.edges[(origin, destination)].get_pheromony()

    def get_path_cost(self, path):
        cost = 0
        for vertice_index in range(self.num_vertices - 1):
            cost += self.get_edge_cost(path[vertice_index], path[vertice_index + 1])

        cost += self.get_edge_cost(path[-1], path[0])
        return cost

    def generate_full_graph(self, cost_matrix=None, random_cost = False):
        for i in range(0, self.num_vertices):
            for j in range(0, self.num_vertices):
                if i != j:
                    if random_cost:
                        cost = random.randint(1, 10)
                    else:
                        cost = cost_matrix[i][j]
                    self.add_edge(i, j, cost)

    def generate_aircraft_graph(self, runaways, aircrafts, cost_matrix = None):
        """
        Generate a graph for Aircraft Landing Problem.
        :param runaways: amount of runaways
        :param aircrafts: amount of available aircraft
        :param cost_matrix:
        :return: None
        """

        for runaway in range(runaways):
            # Add initial dummy node
            runaway_name = f'R{runaway}'
            self.add_edge('D', runaway_name, 0)
            for aircraft in range(aircrafts):
                aircraft_name =  f'A{aircraft}'
                self.add_edge(runaway_name, aircraft_name, -1)
                # Add finish dummy node
                self.add_edge(f'A{aircraft}', 'F', 0)

        #connect dummy nodes
        self.add_edge('D', 'F', 0)