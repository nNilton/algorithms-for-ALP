from decimal import Decimal

import numpy as np
import matplotlib.pyplot as plt
import time

from algorithms_ALP.src.algorithms.ACO.entity.AntALP import AntALP


class AntColonySolverALP:
    """
    Ant Colony Optimization for Aircraft Landing Problem.
    """

    def __init__(self, runaway_number, number_of_ants, evaporation_rate, pheromony_intensity,
                 beta_evaporation_rate, alpha=1, beta1=1, beta2=1):
        """
        Traverses a graph and finds either the max or min distance between nodes.
            :param colony: List of Ants to traverse the graph
            :param evaporation_rate: rate at which pheromone evaporates
            :param pheromony_intensity: constant added to the best path
            :param alpha: weighting of pheromone
            :param beta1: weighting of heuristic (priority)
            :param beta2: weighting of heuristic (cost penality)
            :param beta_evaporation_rate: rate at which beta decays (optional)
        """

        # Main parameters
        self.runaway_number = runaway_number
        self.number_of_ants = number_of_ants
        self.colony = None
        self.evaporation_rate = evaporation_rate
        self.pheromony_intensity = pheromony_intensity
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.beta_evaporation_rate = beta_evaporation_rate

        # Internal representations
        self.pheromone_matrix = None
        self.heuristic_matrix = None
        self.probability_matrix = None
        self.prob_runaway_matrix = None
        self.prob_aircraft_matrix = None

        self.map = None
        self.set_of_available_nodes = None

        # Internal stats
        self.best_series = []
        self.best = None
        self.fitted = False
        self.best_path = None
        self.fit_time = None

    def initialize_solver(self, map_matrix):
        self.create_colony()
        self.map = map_matrix
        assert self.map.shape[0] == self.map.shape[1], "Map is not a distance matrix!"
        num_nodes = self.map.shape[0] + runaway_amount + 2 #nodes D and F
        self.pheromone_matrix = np.ones((num_nodes, num_nodes))
        # Remove the diagonal since there is no pheromone from node i to itself
        self.pheromone_matrix[np.eye(num_nodes) == 1] = 0
        self.heuristic_matrix = 1 / self.map
        self.probability_matrix = (self.pheromone_matrix ** self.alpha) * (
                self.heuristic_matrix ** self.beta1)  # element by element multiplcation
        self.set_of_available_nodes = list(range(num_nodes))
        x = 0

    def create_colony(self):
        self.colony = [AntALP('0') for ant in range(self.number_of_ants)]

    def update_probabilities(self):
        pass

    def choose_next_node(self):
        pass

    def evaluate_solution(self, paths):
        """
        Evaluates the solutions of the ants by adding up the distances total nodes.
        :param paths: solutions from the ants
        :param mode: max or min
        :return: x and y coordinates of the best path as a tuple, the best path, and the best score
        :return:
        """
        scores = np.zeros(len(paths))
        coordinates_i = []
        coordinates_j = []
        for index, path in enumerate(paths):
            cur_score = 0
            coords_i = []
            coords_j = []
            for i in range(len(path) - 1):
                coords_i.append(path[i])
                coords_j.append(path[i + 1])
                cur_score += self.map[path[i], path[i + 1]]
            scores[index] = cur_score
            coordinates_i.append(coords_i)
            coordinates_j.append(coords_j)
            best = np.argmin(scores)

        return (coordinates_i[best], coordinates_j[best]), paths[best], scores[best]

    def start_solver(self, map_matrix, iterations=100):
        candidates_list = []
        affected_list = []
        iter_completed = 0
        brute_stop = False
        start = time.time()
        self.initialize_solver(map_matrix)  # step 1

        for cur_iteration in range(iterations):
            start_iter = time.time()
            if len(candidates_list) > 0 or brute_stop:
                for ant in self.colony:  # step 2
                    self.runaway_selection(ant)
                    sel_aircraft = self.aircraft_selection(ant)
                    affected_list.append(sel_aircraft)
                    candidates_list.remove(sel_aircraft)
                    self.assign_landing_time()

                self.best_series.append(None)
                self.update_pheromone_trail()  # step 3
                iter_completed = cur_iteration
            finish_iter = time.time()
            # go to next iteration
        finish = time.time()

    def update_pheromone_trail(self, paths):
        self.evaporate_pheromony()  # step 1
        self.increase_pheromony(paths)  # step 2

    def increase_pheromony(self, paths):
        """
        Increases the pheromony by some scalar for the best route.
        'r' represents the runaway and j the aircraft choosen.
        :param paths: x and y (r and j) coordinates of the best route
        :return: None
        """
        for path in paths:
            r = path[0]
            j = path[1]
            self.pheromone_matrix[r, j] += self.pheromony_intensity

    def evaporate_pheromony(self):
        """
        Evaporate some pheromone as the inverse of the evaporation rate.
        :return: None
        """
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        self.heuristic_beta *= (1 - self.beta_evaporation_rate)

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
                        self.colony, self.evaporation_rate, self.pheromone_intensification, self.heuristic_alpha,
                        self.heuristic_beta, self.beta_evaporation_rate, self.choose_best, self.fit_time // 60,
                        ["\nStopped Early!" if self.stopped_early else ""][0]),
                    bbox={'facecolor': 'gray', 'alpha': 0.8, 'pad': 10}, transform=ax.transAxes)
            ax.legend()
            plt.title("Ant Colony Optimization Results (best: {})".format(np.round(self.best, 2)))
            plt.show()

    ##Specific operations of ALP
    def runaway_selection(self, ant, candidates_list):  # First probability
        self.runaway_probability()
        pass

    def runaway_probability(self, ant: AntALP, candidates_list, earliest_plane, separation_times):
        """
        Calculate probability of Ant K choose the runaway R.
        :param ant:
        :param candidates_list:
        :return:
        """

        earliest_plane_time = Decimal(earliest_plane['landing_time'])
        earliest_plane_index = earliest_plane['index']
        j = 0

        separation_time = separation_times[earliest_plane_index][j]
        np.argmin(earliest_plane_time + separation_time)

        q = np.random.random(0, 1) # is a value taken randomly into [0,1]
        q0 = 1 # is a constant of the algorithm to ensure the diversification
        r0 = 0 # is an index chosen randomly in {1, …, R}

        np.argmin()
        self.run

        if q < q0:
            #calcular probabilidade
            self.prob_runaway_matrix = None
            pass

        return r0 #otherwise

        probability = None


        pass

    def aircraft_selection(self):
        return None

    def aircraft_probability(self):
        pass

    def assign_landing_time(self):
        pass

    def adjust_landing_time(self):
        pass
