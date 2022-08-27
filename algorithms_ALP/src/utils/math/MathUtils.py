import numpy as np
import random


class MathUtils:
    def __init__(self):
        pass

    @staticmethod
    def generate_random_quadratic_matrix(size, minDist, maxDist):
        stuffs = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                if j > i:
                    stuffs[i, j] = random.randint(minDist, maxDist)
                elif j < i:
                    stuffs[i, j] = stuffs[j, i]
        return stuffs

    @staticmethod
    def generate_quadratic_matrix(size, distance_matrix):
        stuffs = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                if j > i:
                    stuffs[i, j] = distance_matrix[i][j]
                elif j < i:
                    stuffs[i, j] = stuffs[j, i]
        return stuffs

    @staticmethod
    def matrix_list_to_np_array(matrix):
        return np.array(matrix)