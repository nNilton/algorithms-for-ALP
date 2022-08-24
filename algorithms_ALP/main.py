from algorithms_ALP.src.ALPParser import ALPParser
from algorithms_ALP.src.utils.handlers.DataFrameHandler import DataFrameHandler
from algorithms_ALP.src.utils.handlers.FileHandler import FileHandler

if __name__ == '__main__':
    content = FileHandler.read_file('D:\\testing\\airland13.txt', read_mode='r')
    alp_parser = ALPParser()
    status, parsed_content = alp_parser.parser(content)
    if status:
        df = DataFrameHandler.dict_to_df(parsed_content)
        DataFrameHandler.save_df_to_csv(df, 'airland')