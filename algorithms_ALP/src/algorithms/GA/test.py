
from algorithms_ALP.src.utils.handlers.DataFrameHandler import DataFrameHandler
from algorithms_ALP.src.algorithms.ACO.ALPInstance import ALPInstance
from algorithms_ALP.src.algorithms.GA.GASolver import GASolver


path = 'E:\\Repositorios-Git\\algorithms-for-ALP\\algorithms_ALP\\src\\algorithms\\GA\\airland_1659880658268691500.csv'

df = DataFrameHandler.read_csv_data(path)
alp = ALPInstance(df)
alp.build_ALP_instance()
print(alp.aircraft_times)

aco_solver = GASolver(
        runaway_number=1,
        total_aircrafts=3,
        total_population=2)
aco_solver.start(alp_instance=alp)