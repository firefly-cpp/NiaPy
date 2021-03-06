# encoding=utf8
# This is temporary fix to import module from parent folder
# It will be removed when package is published on PyPI
import sys

sys.path.append('../')

import numpy as np
from niapy.task import Task
from niapy.problems import Problem
from niapy.algorithms.basic import GreyWolfOptimizer


# our custom problem class
class MyProblem(Problem):
    def __init__(self, dimension, lower=-10, upper=10, *args, **kwargs):
        super().__init__(dimension, lower, upper, *args, **kwargs)

    def _evaluate(self, x):
        return np.sum(x ** 2)


# we will run 10 repetitions of Grey Wolf Optimizer against our custom MyProblem problem.
my_problem = MyProblem(20)
for i in range(10):
    task = Task(problem=my_problem, max_iters=100)

    # parameter is population size
    algo = GreyWolfOptimizer(population_size=20)

    # running algorithm returns best found minimum
    best = algo.run(task)

    # printing best minimum
    print(best[-1])
