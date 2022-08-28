from algorithms_ALP.src.utils.handlers.DataFrameHandler import DataFrameHandler
from algorithms_ALP.src.utils.math.MathUtils import MathUtils
import ast

class ALPInstance:
    """
    Build an instance of ALP to be solved by optimization algorithm.
    """
    def __init__(self, df_data):
        self.df_data = df_data
        self.separation_times_matrix = None
        self.aircraft_times = {}

    def build_ALP_instance(self):
        separation_times_list = []

        for index, aircraft_row in self.df_data.iterrows():
            self.aircraft_times[f'{str(index)}'] = {
                'appearance_time': aircraft_row['appearance_time'],
                'earliest_landing_time': aircraft_row['earliest_landing_time'],
                'target_landing_time': aircraft_row['target_landing_time'],
                'latest_landing_time': aircraft_row['penality_cost_latest'],
                'penality_cost_earliest': aircraft_row['penality_cost_latest'],
                'penality_cost_latest': aircraft_row['penality_cost_latest']
            }
            list_aux = [float(time) for time in ast.literal_eval(aircraft_row['separation_times'])]
            separation_times_list.append(list_aux)

        self.separation_times_matrix = MathUtils.matrix_list_to_np_array(separation_times_list)


# df = DataFrameHandler.read_csv_data('C:\\Users\\mathe\\Desktop\\workspace\\algorithms-aircraft-landing-problems\\algorithms_ALP\\tmp\\airland_1659880658268691500.csv')
# alp = ALPInstance(df)
# alp.build_ALP_instance()