import pandas as pd
import os


class DataFrameHandler:
    def __init__(self):
        pass

    @staticmethod
    def read_csv_data(file_path, usecols=[]):
        try:
            data = pd.read_csv(file_path, sep=',', skipinitialspace=True, usecols=usecols)
            return data
        except Exception as ex:
            raise BaseException(f'Failed to read data\n {str(ex)}')

    @staticmethod
    def save_df_to_csv(data_frame, file_path):

        path = 'tmp/'

        try:
            os.mkdir(path)
        except:
            pass

        if data_frame and not data_frame.empty:
            data_frame.to_csv(file_path)
            return True

        return False
