from algorithms_ALP.src.ALPParser import ALPParser
from algorithms_ALP.utils.handlers.FileHandler import FileHandler


if __name__ == '__main__':
    content = FileHandler.read_file('D:\\testing\\airland2.txt', read_mode='r')
    alp_parser = ALPParser()
    status, parsed_content = alp_parser.parser(content)
    if status:
        FileHandler.save_file('D:\\testing\\airland_process1.txt', file_object=str(parsed_content), save_mode='w')