from algorithms_ALP.src.ALPParser import ALPParser
from algorithms_ALP.src.algorithms.ACO.AntColonySolverALP import AntColonySolverALP
from algorithms_ALP.src.algorithms.ACO.ALPInstance import ALPInstance
from algorithms_ALP.src.utils.handlers.DataFrameHandler import DataFrameHandler

if __name__ == '__main__':
    df = DataFrameHandler.read_csv_data('C:\\Users\\mathe\\Desktop\\workspace\\algorithms-aircraft-landing-problems\\algorithms_ALP\\tmp\\airland_1659880658268691500.csv')
    alp = ALPInstance(df)
    alp.build_ALP_instance()

    aco_solver = AntColonySolverALP(runaway_number=3, number_of_ants=15, evaporation_rate=1, pheromony_intensity=1,
                 beta_evaporation_rate=.1, alpha=1, beta1=1, beta2=1)
    aco_solver.start_solver(map_matrix=alp.separation_times_matrix)

    x = 0



    # content = FileHandler.read_file('D:\\testing\\airland13.txt', read_mode='r')
    # alp_parser = ALPParser()
    # status, parsed_content = alp_parser.parser(content)
    # if status:
    #     df = DataFrameHandler.dict_to_df(parsed_content)
    #     DataFrameHandler.save_df_to_csv(df, 'airland')
