import numpy as np
import random


class MathUtils:
    """
    Provides basic Math operations for ALP algorithms.
    """
    def __init__(self):
        pass

    @staticmethod
    def generate_random_square_matrix(size: int, min_dist: int, max_dist: int):
        stuffs = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                if j > i:
                    stuffs[i, j] = random.randint(min_dist, max_dist)
                elif j < i:
                    stuffs[i, j] = stuffs[j, i]
        return stuffs

    @staticmethod
    def generate_square_matrix(size: int, distance_matrix: list):
        stuffs = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                if j > i:
                    stuffs[i, j] = distance_matrix[i][j]
                elif j < i:
                    stuffs[i, j] = stuffs[j, i]
        return stuffs

    @staticmethod
    def matrix_list_to_np_array(matrix: list):
        return np.array(matrix)

    @staticmethod
    def join_lists_to_np_array(data_list: list):
        return np.array([data for data in data_list])