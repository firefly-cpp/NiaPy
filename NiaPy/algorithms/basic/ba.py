# encoding=utf8
# pylint: disable=mixed-indentation, multiple-statements, attribute-defined-outside-init, logging-not-lazy, no-self-use, line-too-long, singleton-comparison, arguments-differ, bad-continuation
import logging
from numpy import full, apply_along_axis, argmin
from NiaPy.algorithms.algorithm import Algorithm

logging.basicConfig()
logger = logging.getLogger('NiaPy.algorithms.basic')
logger.setLevel('INFO')

__all__ = ['BatAlgorithm']

class BatAlgorithm(Algorithm):
	r"""Implementation of Bat algorithm.

	**Algorithm:** Bat algorithm

	**Date:** 2015

	**Authors:** Iztok Fister Jr., Marko Burjek and Klemen Berkovič

	**License:** MIT

	**Reference paper:** Yang, Xin-She. "A new metaheuristic bat-inspired algorithm." Nature inspired cooperative strategies for optimization (NICSO 2010). Springer, Berlin, Heidelberg, 2010. 65-74.
	"""
	Name = ['BatAlgorithm', 'BA']
	NP, A, r, Qmin, Qmax = 40, 0.5, 0.5, 0.0, 2.0

	@staticmethod
	def typeParameters(): return {
			'NP': lambda x: isinstance(x, int) and x > 0,
			'A': lambda x: isinstance(x, (float, int)) and x > 0,
			'r': lambda x: isinstance(x, (float, int)) and x > 0,
			'Qmin': lambda x: isinstance(x, (float, int)),
			'Qmax': lambda x: isinstance(x, (float, int))
	}

	def setParameters(self, NP=40, A=0.5, r=0.5, Qmin=0.0, Qmax=2.0, **ukwargs):
		r"""Set the parameters of the algorithm.

		**Arguments:**

		NP {integer} -- population size

		A {decimal} -- loudness

		r {decimal} -- pulse rate

		Qmin {decimal} -- minimum frequency

		Qmax {decimal} -- maximum frequency
		"""
		self.NP, self.A, self.r, self.Qmin, self.Qmax = NP, A, r, Qmin, Qmax
		if ukwargs: logger.info('Unused arguments: %s' % (ukwargs))

	def initPopulation(self, task):
		S, Q, v = full([self.NP, task.D], 0.0), full(self.NP, 0.0), full([self.NP, task.D], 0.0)
		Sol = task.Lower + task.bRange * self.uniform(0, 1, [self.NP, task.D])
		Fitness = apply_along_axis(task.eval, 1, Sol)
		return Sol, Fitness, {'S': S, 'Q':Q, 'v':v}

	def runIteration(self, task, Sol, Fitness, xb, fxb, S, Q, v, **dparams):
		for i in range(self.NP):
			Q[i], v[i], S[i] = self.Qmin + (self.Qmax - self.Qmin) * self.uniform(0, 1), v[i] + (Sol[i] - xb) * Q[i], task.repair(Sol[i] + v[i], rnd=self.Rand)
			if self.rand() > self.r: S[i] = task.repair(xb + 0.001 * self.normal(0, 1, task.D), rnd=self.Rand)
			Fnew = task.eval(S[i])
			if (Fnew <= Fitness[i]) and (self.rand() < self.A): Sol[i], Fitness[i] = S[i], Fnew
		return Sol, Fitness, {'S': S, 'Q':Q, 'v':v}

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
