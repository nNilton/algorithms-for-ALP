import random

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

    def generate_graph(self, cost_matrix=None):
        for i in range(1, self.num_vertices + 1):
            for j in range(1, self.num_vertices + 1):
                if i != j:
                    cost = random.randint(1, 10)
                    # cost = cost_matrix[i][j]
                    self.add_edge(i, j, cost)
