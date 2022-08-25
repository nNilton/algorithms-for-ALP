

class AntALP:
    """
    Defines an Ant for Aircraft Landing Problem.
    """

    def __init__(self, runaway):
        """
        :param runaway:
        """
        self.runaway = runaway
        self.solution = []
        self.cost = None

    def get_runaway(self):
        return self.runaway

    def set_runaway(self, runaway):
        self.runaway = runaway

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

