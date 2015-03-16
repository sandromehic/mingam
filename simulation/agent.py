import strategy
import logging as log
import uuid
from random import randrange
from numpy import sign

class Agent:
	def __init__(self, agentType):		
		self.type = agentType
		self.id = self.generateID()
		self.history = []		
		self.score = 0
		self.verbose = False
		log.info("Creating agent of type " + self.type)
		log.info(self.id)

	def generateID(self):
		return uuid.uuid4()

	def makeDecision(self, game):
		pass

	def __str__(self):
		return "Agent %s!" % self.id

class ClassicAgent(Agent):
	def __init__(self, brainSize, nStrats):
		Agent.__init__(self, "classical")

		# memory available to the agent
		self.brainSize = brainSize
		# number of strategies
		self.nStrats = nStrats
		# invoke methods to generate strategies
		self.strats = []
		# decision and history
		self.decision = 0
		# dHistory is a list of tuple (roundNumber, agentDecision)
		self.dHistory = []

		self.generateStrats()

	def generateStrats(self):
		for i in range(self.nStrats):
			self.strats.append( strategy.ClassicStrat( self.brainSize ) )

		log.info("Strategies generated: ")
		log.info(self.strats)

	def makeDecision(self, game):
		#list for virtual scores
		vscores = []
		# run all possible strategies
		for s in self.strats:
			# index from which the history is relevant to strategy (brainsize)
			# don't pass useless history, only the latest
			fromIdx = len(game.history) - self.brainSize
			s.calculateDecision(game.history[fromIdx:])
			vscores.append(s.getVScore())

		# find the best strategy and its decision
		bestStrats = []
		m = max(vscores)
		for (i, s) in enumerate(self.strats):
			if(s.getVScore() == m):
				bestStrats.append(i)

		if(len(bestStrats) == 0):
			# error, no best strategy
			log.error("No best strategy available")
		elif(len(bestStrats) == 1):
			# only one best strategy, use it
			self.decision = self.strats[bestStrats[0]].getDecision()
			# print "Agent {} using strategy {}".format(self.id, bestStrats[0])
		else:
			# more than 1 best strategy, choose one randomly
			rndStrat = randrange(0, len(bestStrats))
			self.decision = self.strats[bestStrats[rndStrat]].getDecision()
			# print "Agent {} using strategy {}".format(self.id, bestStrats[rndStrat])

		# log.info("Agent made the decision!")
		# log.info(self.decision)

		# # update various stuff around agent and strategy class
		# self.updateState(game)

	def updateState(self, game):
		# add current decision to the agents history
		self.dHistory.append((game.round, self.decision))
		# update the score, if agent won +1 or -1 if lost
		correctDecision = 1 if ( game.attendance[-1][1] <= (len(game.agents)/2) ) else 0
		if self.decision == correctDecision:
			self.score += 1
		else:
			self.score -= 1
		# update all the strategy scores
		for s in self.strats:
			s.updateState(game.round, correctDecision)

		if(self.verbose):
			f = open('../agent', 'a')
			f.write("Round number: {}\n".format(game.round))
			f.write("Global history: {}\n".format(game.history[len(game.history)-self.brainSize:]))
			f.write("Decision made: {}\n".format(self.decision))
			for s in self.strats:
				f.write("Strategy: {}\n".format(s.strat))
				f.write("Strategy score: {}\n".format(s.getVScore()))
				f.write("Strategy decision: {}\n".format(s.decision))
				f.write("----------------------------------------\n")

			f.write("____________________________________________\n")

	def getDecision(self):
		return self.decision