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
import math
import random
import numpy

from algorithms_ALP.src.algorithms.ACO.ALPInstance import ALPInstance
from algorithms_ALP.src.algorithms.ACO.entity.Aircraft import Aircraft
from algorithms_ALP.src.algorithms.GA.model.Individual import Individual

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
        self.individuals = []
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
        for i in range(self.total_population):
            #random_numbers = numpy.random.uniform(low=0, high=1, size=self.total_aircrafts)
            random_numbers = numpy.random.randint(low=1, high=99, size=self.total_aircrafts)/100
            print(random_numbers)
            self.individuals.append(Individual(i, random_numbers, -1, -1, -1, -1))
            self.evaluate_fitness(i)
            self.evaluate_unfitness(i)


    def evaluate_fitness(self, index):
        worst_index = -1
        worst_value = -1
        fitness = 0
        for i in range (0,self.total_aircrafts):
            earliest_landing_time = self.global_aircraft_candidates[i].earliest_landing_time
            latest_landing_time = self.global_aircraft_candidates[i].latest_landing_time
            scheduled_time = int(earliest_landing_time + (self.individuals[index].genes[i] * (latest_landing_time - earliest_landing_time)))
            deviation = scheduled_time - self.global_aircraft_candidates[i].target_landing_time
            if(deviation > 0):
                cost = deviation * self.global_aircraft_candidates[i].penality_cost_earliest
                if (cost > worst_value):
                    worst_index = i
                    worst_value = cost
                fitness += cost
            else:
                cost = deviation * self.global_aircraft_candidates[i].penality_cost_latest * -1
                if (cost > worst_value):
                    worst_index = i
                    worst_value = cost
                fitness += cost
        self.individuals[index].worst_chromosome_index = worst_index
        self.individuals[index].worst_chromosome_value = worst_value
        self.individuals[index].fitness = fitness

    def binary_tournment(self):
        rand1 = random.randrange(self.total_population)
        rand2 = random.randrange(self.total_population)#this can return the same element twice fix this if it was necessary
        if(self.individuals[rand1].unfitness<self.individuals[rand2].unfitness):
            return self.individuals[rand1].genes
        elif(self.individuals[rand1].unfitness>self.individuals[rand2].unfitness):
            return self.individuals[rand2].genes
        else:
            if(self.individuals[rand1].fitness>=self.individuals[rand2].fitness):
                #print(self.individuals[rand1].fitness)
                return self.individuals[rand1].genes
            else:
                #print(self.individuals[rand2].fitness)
                return self.individuals[rand2].genes

    def crossover(self):
        parent1 = self.binary_tournment()
        parent2 = self.binary_tournment()
        child = []
        for i in range(0, self.total_aircrafts):
            if(random.randrange(2)==0):
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        individual = Individual(self.total_population, child, -1, -1, -1, -1)
        self.individuals.append(individual)
        self.evaluate_fitness(self.total_population)
        self.evaluate_unfitness(self.total_population)
        self.mutation(individual)

    def mutation(self, individual):
        current_fitness = individual.worst_chromosome_index
        print("pior: ", individual.worst_chromosome_value)
        print("total: ", individual.fitness)
        #if(current_fitness > 60000):
         #   current_fitness = 60000
        prob = math.sqrt(individual.worst_chromosome_value / individual.fitness)
        rest = 1 - prob
        result = numpy.random.choice(['a', 'b'], 1, p=[prob, rest])
        if(result == 'a'):
            #individual.genes[random.randrange(self.total_aircrafts)] = numpy.random.uniform(low=0, high=1)
            individual.genes[individual.worst_chromosome_index] = numpy.random.randint(low=1, high=99)/100
            self.evaluate_fitness(individual.index)
            self.evaluate_unfitness(individual.index)


    def evaluate_unfitness(self, index):
        unfitness = 0
        for i in range(0, self.total_aircrafts):
            for j in range(0, self.total_aircrafts):
                if(i != j):
                    earliest_landing_time = self.global_aircraft_candidates[i].earliest_landing_time
                    latest_landing_time = self.global_aircraft_candidates[i].latest_landing_time
                    scheduled_time_i = int(earliest_landing_time + (self.individuals[index].genes[i] * (latest_landing_time - earliest_landing_time)))

                    earliest_landing_time = self.global_aircraft_candidates[j].earliest_landing_time
                    latest_landing_time = self.global_aircraft_candidates[j].latest_landing_time
                    scheduled_time_j = int(earliest_landing_time + (self.individuals[index].genes[j] * (latest_landing_time - earliest_landing_time)))

                    if(scheduled_time_i <= scheduled_time_j):
                        delta = scheduled_time_j - scheduled_time_i
                        unfitness += max(0, self.separation_times_matrix[i,j] - delta)
        #print(unfitness)
        self.individuals[index].unfitness = unfitness

    def build_population_groups(self, reference_fitness, reference_unfitness):
        g1 = []
        g2 = []
        g3 = []
        g4 = []
        for i in self.individuals:
            if(i.unfitness > reference_unfitness):
                if (i.fitness < reference_fitness):
                    g1.append(i)
                else:
                    g2.append(i)
            else:
                if(i.fitness > reference_fitness):
                    g3.append(i)
                else:
                    g4.append(i)
        return g1,g2,g3,g4

    def population_replacement(self):
        child = self.individuals.pop(self.total_population)
        group1, group2, group3, group4 = self.build_population_groups(child.fitness, child.unfitness)
        if(len(group1) > 0):
            selected_element = random.choice(group1)
        elif(len(group2) >0):
            selected_element = random.choice(group2)
        elif (len(group3) > 0):
            selected_element = random.choice(group3)
        else:
            selected_element = random.choice(group4)
        child.index = selected_element.index
        self.individuals[selected_element.index] = child

    def find_best_solution(self):
        candidate = Individual(-1, [-1], 9999999, 1, -1, -1)
        for i in self.individuals:
            if((i.fitness < candidate.fitness) and (i.unfitness <= candidate.unfitness)):
                candidate = i
            else:
                continue
        return candidate

    def list(self):
        print("-----------------------")
        for i in self.individuals:
            print("Indice: ",i.index)
            print(i.genes)
            print("Custo: ", i.fitness)
            print("Inviabilidade: ",i.unfitness)

    def start(self, alp_instance: ALPInstance, max_iterations=10):
        self.__initialize(alp_instance)
        self.generate_initial_population()
        for i in range(0, max_iterations):
            self.crossover()
            self.population_replacement()
        self.list()
        return self.find_best_solution()