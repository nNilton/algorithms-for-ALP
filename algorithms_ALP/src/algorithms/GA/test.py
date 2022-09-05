
from algorithms_ALP.src.utils.handlers.DataFrameHandler import DataFrameHandler
from algorithms_ALP.src.algorithms.ACO.ALPInstance import ALPInstance
from algorithms_ALP.src.algorithms.GA.GASolver import GASolver


path = 'E:\\Repositorios-Git\\algorithms-for-ALP\\algorithms_ALP\\src\\algorithms\\GA\\airland_1659880658268691500.csv'

df = DataFrameHandler.read_csv_data(path)
alp = ALPInstance(df)
alp.build_ALP_instance()

aco_solver = GASolver(
        runaway_number=1,
        total_aircrafts=100,
        total_population=500)
f = aco_solver.start(alp_instance=alp, max_iterations=1000000)
print(f.genes)
print(f.fitness)
print(f.unfitness)
print(f.index)