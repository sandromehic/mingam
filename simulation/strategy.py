
import logging as log
import numpy.random as nprnd
from numpy import sign

class Strategy:
	def __init__(self, strategyType):
		self.type = strategyType
		self.vScore = 0
		self.rScore = 0

class ClassicStrat(Strategy):
	def __init__(self, brainSize):
		Strategy.__init__(self, "classical")
		log.info("Creating classical strategy of brainsize %s" % brainSize)
		self.brainSize = brainSize
		self.strat = []
		self.decision = 0
		self.dHistory = []
		self.generateStrategy()

	def __str__(self):
		return self.strat

	def generateStrategy(self):
		# generate random strategy that is saved as a list of 
		# of length 2^brainSize containing 1's and 0's
		nprnd.seed()
		self.strat = nprnd.randint(2,size=2**self.brainSize)

		log.info("Stategy generated: ")
		log.info(self.strat)

	def calculateDecision(self, hist):
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
		
	def updateState(self, round, correctDecision):
		# payoff function is an increase or decrease by 1
		# if the strategy made the right decision
		self.dHistory.append((round, self.decision))
		if (self.decision == correctDecision): 
			self.vScore += 1
		else:
			self.vScore -= 1

	def getVScore(self):
		return self.vScore

	def getDecision(self):
		return self.decision

	def getStrat(self):
		return self.strat