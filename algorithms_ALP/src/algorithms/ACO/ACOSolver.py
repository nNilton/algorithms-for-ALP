#  MIT License
#
#  Copyright (c) 2022 Matheus Phelipe Alves Pinto
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from algorithms_ALP.src.algorithms.ACO.ALPInstance import ALPInstance
from algorithms_ALP.src.algorithms.ACO.entity.Ant import Ant
from algorithms_ALP.src.algorithms.ACO.entity.Aircraft import Plane
from algorithms_ALP.src.algorithms.ACO.entity.Runaway import Runaway
from algorithms_ALP.src.utils.math.MathUtils import MathUtils

import numpy as np
import random
from datetime import datetime


class ACOSolver:
    """
    Ant Colony Optimization for Aircraft Landing Problem.
    """

    def __init__(self, runaway_number, number_of_ants, evaporation_rate, pheromone_intensity,
                 beta_evaporation_rate, alpha=1, beta1=1, beta2=1):
        """
        :param runaway_number: amount of runways available
        :param number_of_ants: amount of Ants to build solutions
        :param evaporation_rate: rate at which pheromone evaporates
        :param pheromone_intensity: constant added to the best path
        :param beta_evaporation_rate: rate at which beta decays (optional)
        :param alpha: weighting of pheromone
        :param beta1: weighting of heuristic (priority)
        :param beta2: weighting of heuristic (cost penality)
        """

        # Configurable parameters
        self.runaway_number = runaway_number
        self.number_of_ants = number_of_ants
        self.evaporation_rate = evaporation_rate
        self.pheromone_rate = pheromone_intensity
        self.beta_evaporation_rate = beta_evaporation_rate
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.separation_times_matrix = None

        # Internal parameters
        self.colony = None
        self.global_aircraft_candidates = []
        self.global_runaway_list = []
        self.pheromone_matrix = None

    def __initialize(self, alp_instance: ALPInstance = None):
        """
        Initialize internal parameters of ACO.
        :param alp_instance:
        :return:
        """

        try:
            self.global_runaway_list = [
                Runaway(run_index, runaway_name=f'R{run_index}') for run_index in range(self.runaway_number)
            ]
            # Create global aircraft candidate list with index
            self.global_aircraft_candidates = [
                Plane(int(index_plane), airplane_data) for index_plane, airplane_data in
                alp_instance.aircraft_times.items()
            ]

            # Start colony with initial data (there are not any solution)
            self.colony = [
                Ant(ant_id = ant_id, plane_candidates_list=self.global_aircraft_candidates, runaways_list=self.global_runaway_list)
                for ant_id in range(self.number_of_ants)
            ]

            # Create pheromony matrix (considering runaways and dummy nodes)
            matrix_dimension = self.runaway_number + len(
                alp_instance.aircraft_times) + 2  # (2) Dummy nodes called D and F
            self.pheromone_matrix = self.create_matrix_list(matrix_dimension, len(alp_instance.aircraft_times))

            # Load separation times matrix
            self.separation_times_matrix = alp_instance.separation_times_matrix


        except Exception as ex:
            raise ex

    def start(self, alp_intance: ALPInstance, max_iterations=10):
        self.__initialize(alp_intance)
        global_start = datetime.now()
        for iteration in range(max_iterations):
            iter_start = datetime.now()
            print(f"Starting iteration {int(iteration + 1)} / {max_iterations} expected")
            for ant in self.colony:
                runaway_selected = self.select_runaway(ant)
                self.select_aircraft(ant, runaway_selected)
                pass

            iter_finish = datetime.now()
            print(f"Finish iteration [{int(iteration)}]: Elapsed {iter_finish - iter_start} seconds")

        global_finish = datetime.now()
        print(f"Finish iteration [{int(iteration)}]: Elapsed {global_finish - global_start} seconds")

    def create_matrix_list(self, matrix_dimension, planes_size):
        """
        Create the adjacency matrix that represents Graph's path for ALP.
        :param matrix_dimension: square dimension (containing dummy nodes)
        :param planes_size: amount of planes
        :return: ndarray
        """
        matrix = []

        # Create connections between dummy node D and runways
        aux_list = [0]
        aux_list = MathUtils.join_lists(aux_list, [1] * self.runaway_number)
        aux_list = MathUtils.join_lists(aux_list, [0] * (planes_size + 1))
        matrix.append(aux_list)

        # Create connections between runaways and aircrafts
        for runaway in range(self.runaway_number):
            aux_list = [0]
            aux_list = MathUtils.join_lists(aux_list, [0] * self.runaway_number)
            aux_list = MathUtils.join_lists(aux_list, [1] * planes_size)
            aux_list.append(0)
            matrix.append(aux_list)

        # Create connections between aircrafts dummy node F
        for runaway in range(planes_size):
            aux_list = [0]
            aux_list = MathUtils.join_lists(aux_list, [0] * (self.runaway_number + planes_size))
            aux_list.append(1)
            matrix.append(aux_list)
        # Create connection between nodes F and D
        aux_list = [1]
        matrix.append(MathUtils.join_lists(aux_list, [0] * (matrix_dimension - 1)))

        np_matrix = MathUtils.matrix_list_to_np_array(matrix)
        assert np_matrix.shape[0] == np_matrix.shape[1] and np_matrix.shape[
            0] == matrix_dimension, "Matrix dimensions wrong!"

        return np_matrix

    def select_runaway(self, ant: Ant):
        """
        For ant k, there is a probability rule to select a runway r, from node D.
        :return: Runaway
        """
        q0 = 5  # 0< q0 < 1 is a constant of the algorithm
        q = random.randint(0, 1)
        r0 = random.choice(self.global_runaway_list)
        if q < q0:
            runaway_cal_list = []
            for runaway in ant.runaways_list:
                if len(runaway.solution_list) > 0:
                    last_plane = runaway.solution_list[-1]  # last aircraft affected to the runway r for the ant
                    last_time_plus_sep_time_list = []
                    for candidate_index in ant.plane_candidates_list:
                        # Separation time between the landings of aircraft i and j if they land on the same runaway
                        separation_time = self.separation_times_matrix[last_plane.index][candidate_index]
                        last_time_plus_sep_time_list.append(last_plane.landing_time + separation_time)

                    runaway_cal_list.append(min(last_time_plus_sep_time_list))
                else:
                    return r0

            return min(runaway_cal_list)

        return r0

    def select_aircraft(self, ant: Ant, runaway_selected: Runaway):
        """
        After choosing a runway r, the ant has to select an aircraft to land on this runway.
        :param ant:
        :param runaway_selected:
        :return: Aircraft
        """
        print(f"Ant with id {ant.ant_id} selected runaway {runaway_selected.runaway_name}")
        pass


# Aeronaves candidatas globais
planes_to_landing = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Cada formiga cria sua lista de aeronaves candidatas

# Iteracao

# Formiga inicia do nó D
# Seleciona pista (carga da pista, qual pista ficará livre mais cedo)
# Seleciona aeronave para pousar (da sua lista de candidatas para pouso) - tal escolha depende da prioridade da aeronave e da memória da colônia
# Formiga volta para nó D, repetir até não ter mais aeronave para pousar (lista local)

# Para cada formiga, com sua lista de aeronaves escolhidas, fazemos:
# fixar os tempos de aterrisagem desta aeronaves
# remover definitivamente da lista global de aeronaves candidatas


# Representacao da formiga: formiga representa uma solução para o problema
"""
Example of an Ant (runaway list)
runaway_name    airplane_index:landing_time
Runway 1        1:125 5:201 4:56 –
Runway 2        2:108 3:184 6:300 8:655
Runway 3        7:54 10:407 9:520 –
"""

# Inicialização do problema
# Criar lista de aeronaves candidatas para cada formiga
# Iniciar lista de runaways como NULL
# Inicializar matrix de feromônio
