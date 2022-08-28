import pandas as pd
import os
import time


class DataFrameHandler:
    def __init__(self):
        pass

    @staticmethod
    def read_csv_data(file_path, usecols=None, sep=';'):
        try:
            data = pd.read_csv(file_path, sep=sep, skipinitialspace=True, usecols=usecols)
            return data
        except Exception as ex:
            raise BaseException(f'Failed to read data\n {str(ex)}')

    @staticmethod
    def dict_to_df(data_dict, orient='index'):
        return pd.DataFrame.from_dict(data_dict, orient=orient)

    @staticmethod
    def save_df_to_csv(data_frame, file_name, file_path=None):

        if file_path is None:
            file_path = os.getcwd() + '/tmp/'
            try:
                os.mkdir(file_path)
            except:
                pass

            file_path = os.path.join(file_path, f'{file_name}_{time.time_ns()}.csv')

        if data_frame.empty is False:
            data_frame.to_csv(file_path, sep=';')
            return True

        return False
