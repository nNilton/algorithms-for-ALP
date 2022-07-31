from algorithms_ALP.src.ALPParser import ALPParser
from algorithms_ALP.utils.handlers.FileHandler import FileHandler


if __name__ == '__main__':
    content = FileHandler.read_file('D:\\testing\\airland1.txt', read_mode='r')
    FileHandler.save_file('D:\\testing\\teste_gravacao.txt', file_object=content, save_mode='w')