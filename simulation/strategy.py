
import logging as log
import numpy.random as nprnd
from numpy import sign

class Strategy:
	def __init__(self, strategyType):
		self.type = strategyType
		self.vScore = 0
		self.rScore = 0
		# decision take at last round (calculated with calculateDecision method
		# and retrieved with getDecision method)
		self.decision = None
		# strategy that is to be initialized inside a child class
		self.strat = []

	def calculateDecision(self, hist):
		# by default, a strategy should have claculateDecision method
		pass

	def getDecision(self):
		return self.decision

	def getVScore(self):
		return self.vScore

	def getRScore(self):
		return self.rScore

	def getStrat(self):
		return self.strat

class ClassicStrat(Strategy):
	def __init__(self, brainSize):
		Strategy.__init__(self, "classical")
		log.info("Creating classical strategy of brainsize %s" % brainSize)
		self.brainSize = brainSize
		self.dHistory = []
		self.generateStrategy()

	def __str__(self):
		rtnString = []
		for i,s in enumerate(self.strat):
			rtnString.extend([str(int(bin(i)[2:])), '->', str(s), '\n'])

		rtn = ' '.join(rtnString)
		return rtn 

	def generateStrategy(self):
		# generate random strategy that is saved as a list of 
		# of length 2^brainSize containing 1's and 0's
		nprnd.seed()
		self.strat = nprnd.randint(2,size=2**self.brainSize)

		log.info("Stategy generated: ")
		log.info(self.strat)

	def calculateDecision(self, hist, verbose=False):
		# history is a list of integers, we convert them to a unified string
		# and then convert to decimal integer that is the index of our strategy
		tmpStr = []
		for x in hist:
			if(x<=0):
				tmpStr.append('0')
			else:
				tmpStr.append('1')

		info = ''.join(tmpStr)
		idx = int(info, 2)
		self.decision = self.strat[idx]

		if verbose:
			print "Local + global {}, index {}".format(info, idx)
			print "Strategy: {}".format(self.strat)
			print "Decision made: {}".format(self.decision) 
			print "Strategy score: {}".format(self.vScore)

		
	def updateState(self, round, correctDecision):
		# payoff function is an increase or decrease by 1
		# if the strategy made the right decision
		self.dHistory.append((round, self.decision))
		if (self.decision == correctDecision): 
			self.vScore += 1
		else:
			self.vScore -= 1

class ZeroStrat(Strategy):
	'''
	This strategy responds with None at every history istance. It is needed
	as a control strategy for Speculator Agents. It increases its virtual score
	at every round by a small amount epsilon, and thus ensures that only the
	strategies that have performed well over time will have higher virtual score
	and will be able to participate in the game.
	'''
	def __init__(self, brainSize, epsilon):
		Strategy.__init__(self, "zero")
		log.info("Creating zero strategy of brainsize %s" % brainSize)
		self.brainSize = brainSize
		self.epsilon = epsilon
		self.generateStrategy()

	def updateState(self, round, correctDecision):
		self.vScore += self.epsilon

	def generateStrategy(self):
		self.strat = [None] * 2**self.brainSize
