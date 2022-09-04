#  MIT License
#
#  Copyright (c) 2022 Nilton Vieira da Silva
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

import random
import numpy

from algorithms_ALP.src.utils.handlers.DataFrameHandler import DataFrameHandler
from algorithms_ALP.src.algorithms.ACO.ALPInstance import ALPInstance
from algorithms_ALP.src.algorithms.ACO.entity.Aircraft import Aircraft

class GASolver:

    def __init__(self, runaway_number, total_aircrafts, total_population):
        """
        :param runaway_number: amount of runways available
        """

        # Configurable parameters
        self.runaway_number = runaway_number
        self.total_aircrafts = total_aircrafts
        self.total_population = total_population
        self.separation_times_matrix = None

        # Internal parameters
        self.global_aircraft_candidates = []
        self.fitness = [-1] * total_population
        # self.global_runaway_list = []

    def __initialize(self, alp_instance: ALPInstance = None):
        """
        Initialize internal parameters of ACO.
        :param alp_instance:
        :return:
        """

        try:
            # Create global aircraft candidate list with index
            self.global_aircraft_candidates = [
                Aircraft(int(index_plane), airplane_data) for index_plane, airplane_data in
                alp_instance.aircraft_times.items()
            ]

            # Load separation times matrix
            self.separation_times_matrix = alp_instance.separation_times_matrix


        except Exception as ex:
            raise ex

    def generate_initial_population(self):
        random_numbers = numpy.random.uniform(low=0, high=1, size=(self.total_population, self.total_aircrafts))
        print(random_numbers)
        return random_numbers

    def evaluate_fitness(self, population, position):
        fitness = 0
        for i in range (0,self.total_aircrafts):
            earliest_landing_time = self.global_aircraft_candidates[i].earliest_landing_time
            latest_landing_time = self.global_aircraft_candidates[i].latest_landing_time
            scheduled_time = (earliest_landing_time + (population[position,i] * (latest_landing_time - earliest_landing_time)))
            deviation = scheduled_time - self.global_aircraft_candidates[i].target_landing_time
            if(deviation > 0):
                fitness += deviation * deviation
            else:
                fitness -= deviation * deviation
        self.fitness[position] = fitness

    def binary_tournment(self, population):
        rand1 = random.randrange(self.total_population)
        rand2 = random.randrange(self.total_population)#this can return the same element twice fix this if it was necessary
        if(self.fitness[rand1]>self.fitness[rand2]):
            return population[rand1]
        else:
            return population[rand2]

    def crossover(self, population):
        parent1 = self.binary_tournment(population)
        parent2 = self.binary_tournment(population)
        print(parent1)
        print(parent2)
        child = []
        for i in range(0, self.total_aircrafts):
            if(random.randrange(2)==0):
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child
        print(self.global_aircraft_candidates)
        test = self.generate_initial_population()
        self.evaluate_fitness(test)