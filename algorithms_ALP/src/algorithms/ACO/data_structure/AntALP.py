

class AntALP:
    """
    Defines an Ant for Aircraft Landing Problem.
    """

    def __init__(self, node):
        """
        :param node:
        """
        self.node = node
        self.solution = []
        self.cost = None

    def get_node(self):
        return self.node

    def set_node(self, node):
        self.node = node

    def get_solution(self):
        return self.solution

    def set_solution(self, solution, cost):
        if self.cost is None:
            self.solution = solution[:]
            self.cost = cost
        elif cost < self.cost:
            self.solution = solution[:]
            self.cost = cost

    def get_cost(self):
        return self.cost

