from algorithms_ALP.src.ALPParser import ALPParser
from algorithms_ALP.src.algorithms.ACO.AntColonySolver import AntColonySolver
from algorithms_ALP.src.algorithms.ACO.data_structure.GraphALP import GraphALP
from algorithms_ALP.src.utils.handlers.DataFrameHandler import DataFrameHandler
from algorithms_ALP.src.utils.handlers.FileHandler import FileHandler
from algorithms_ALP.src.utils.math.MathUtils import MathUtils

if __name__ == '__main__':
    # content = FileHandler.read_file('D:\\testing\\airland13.txt', read_mode='r')
    # alp_parser = ALPParser()
    # status, parsed_content = alp_parser.parser(content)
    # if status:
    #     df = DataFrameHandler.dict_to_df(parsed_content)
    #     DataFrameHandler.save_df_to_csv(df, 'airland')

    problem = MathUtils.generate_random_quadratic_matrix(5, 10, 100)
#     problem = [[0,60,33,17,34,29,42,94,61,41,43,12,59,43,98]
# ,[60,0,60,31,87,71,67,16,38,87,31,66,75,14,67]
# ,[33,60,0,70,55,18,59,41,18,15,65,95,48,92,51]
# ,[17,31,70,0,63,78,63,92,81,78,84,92,33,70,82]
# ,[34,87,55,63,0,84,24,65,51,71,21,14,74,60,19]
# ,[29,71,18,78,84,0,50,82,19,61,56,52,50,60,34]
# ,[42,67,59,63,24,50,0,77,56,74,86,78,13,26,89]
# ,[94,16,41,92,65,82,77,0,32,49,42,76,80,36,14]
# ,[61,38,18,81,51,19,56,32,0,65,71,34,22,17,51]
# ,[41,87,15,78,71,61,74,49,65,0,86,71,28,58,32]
# ,[43,31,65,84,21,56,86,42,71,86,0,41,61,53,15]
# ,[12,66,95,92,14,52,78,76,34,71,41,0,79,13,43]
# ,[59,75,48,33,74,50,13,80,22,28,61,79,0,71,84]
# ,[43,14,92,70,60,60,26,36,17,58,53,13,71,0,73]
# ,[98,67,51,82,19,34,89,14,51,32,15,43,84,73,0]]
#     problem = MathUtils.matrix_list_to_np_array(problem)
    optimizer = AntColonySolver(ants=problem.shape[0], evaporation_rate=.1, pheromony_intensity=2, alpha=1, beta=1,
                                beta_evaporation_rate=0, choose_best=.1)

    best = optimizer.fit(problem, 100)
    x = 0

