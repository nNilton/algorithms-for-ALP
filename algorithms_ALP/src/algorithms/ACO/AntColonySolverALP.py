import numpy as np
import matplotlib.pyplot as plt
import time


class AntColonyALP:
    """
    Ant Colony Optimization for Aircraft Landing Problem.
    """

    def __init__(self,
                 ants, evaporation_rate, pheromony_intensity,
                 beta_evaporation_rate, choose_best, alpha = 1, beta = 1):
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

    def solve(self, map_matrix, iterations=100):
        for cur_iteration in iterations:
            # K ants exists in colony
            for ant in self.ants:
                pass

    def increase_pheromony(self):
        pass

    def evaporate_pheromony(self):
        pass

    def save_results(self):
        pass

    def plot(self):
        """
        Plots the score over time after the model has been fitted.
        :return: None if the model isn't fitted yet
        """
        if not self.fitted:
            print("Ant Colony Optimizer not fitted!  There exists nothing to plot.")
            return None
        else:
            fig, ax = plt.subplots(figsize=(20, 15))
            ax.plot(self.best_series, label="Best Run")
            ax.set_xlabel("Iteration")
            ax.set_ylabel("Performance")
            ax.text(.8, .6,
                    'Ants: {}\nEvap Rate: {}\nIntensify: {}\nAlpha: {}\nBeta: {}\nBeta Evap: {}\nChoose Best: {}\n\nFit Time: {}m{}'.format(
                        self.ants, self.evaporation_rate, self.pheromone_intensification, self.heuristic_alpha,
                        self.heuristic_beta, self.beta_evaporation_rate, self.choose_best, self.fit_time // 60,
                        ["\nStopped Early!" if self.stopped_early else ""][0]),
                    bbox={'facecolor': 'gray', 'alpha': 0.8, 'pad': 10}, transform=ax.transAxes)
            ax.legend()
            plt.title("Ant Colony Optimization Results (best: {})".format(np.round(self.best, 2)))
            plt.show()

    ##Specific operations of ALP

    def runaway_selection(self):
        pass

    def aircraft_selection(self):
        pass

    def assign_landing_time(self):
        pass

    def adjust_landing_time(self):
        pass
