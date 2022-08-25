import numpy as np
import time


# Main stream
#
# Initialization
# Runaway selection
# Aircraft Selection
# Assignment of landing time
# Adjustment of the landing time
# If no more aircraft to land,
#     update the pheromone trails
#     if maximum number of iteractions
#         return optimal solution


class AntColonyALP:
    """
    Ant Colony Optimization for Aircraft Landing Problem.
    """

    def __init__(self,
                 ants, evaporation_rate, pheromony_intensity,
                 alpha, beta, beta_evaporation_rate, choose_best):
        """
        Traverses a graph and finds either the max or min distance between nodes.
            :param ants: number of ants to traverse the graph
            :param evaporation_rate: rate at which pheromone evaporates
            :param pheromony_intensity: constant added to the best path
            :param alpha: weighting of pheromone
            :param beta: weighting of heuristic (1/distance)
            :param beta_evaporation_rate: rate at which beta decays (optional)
            :param choose_best: probability to choose the best route
        """

        # Main parameters
        self.ants = ants
        self.evaporation_rate = evaporation_rate
        self.pheromony_intensity = pheromony_intensity
        self.alpha = alpha
        self.beta = beta
        self.beta_evaporation_rate = beta_evaporation_rate
        self.choose_best = choose_best

        # Internal representations
        self.pheromone_matrix = None
        self.heuristic_matrix = None
        self.probability_matrix = None

        self.map = None
        self.set_of_available_nodes = None

        # Internal stats
        self.best_series = []
        self.best = None
        self.fitted = False
        self.best_path = None
        self.fit_time = None

    def initialize_solver(self):
        pass

    def update_probabilities(self):
        pass

    def choose_next_node(self):
        pass

    def evaluate_solution(self):
        pass

    def fitness(self, map_matrix, iterations=100, mode='min', verbose=True):
        pass

    def increase_pheromony(self):
        pass

    def evaporate_pheromony(self):
        pass

    def save_results(self):
        pass

    ##Specific operations of ALP

    def runaway_selection(self):
        pass

    def aircraft_selection(self):
        pass

    def assign_landing_time(self):
        pass

    def adjust_landing_time(self):
        pass
