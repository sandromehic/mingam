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
		self.score = [0]
		self.verbose = False
		log.info("Creating agent of type " + self.type)
		log.info(self.id)

	def generateID(self):
		return uuid.uuid4()

	def makeDecision(self, game):
		pass

	def generateStrats(self):
		pass

	def __str__(self):
		return "Agent %s!" % self.id

class ClassicAgent(Agent):
	def __init__(self, brainSize, nStrats):
		Agent.__init__(self, "classic")

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

	def getCurrentHistory(self, game):
		fromIdx = len(game.history) - self.brainSize
		return game.history[fromIdx:]

	def makeDecision(self, game):
		#list for virtual scores
		vscores = []
		# run all possible strategies
		for s in self.strats:
			# index from which the history is relevant to strategy (brainsize)
			# don't pass useless history, only the latest
			verb = True if self.verbose else 0
			if verb: print "Agent decision making at round {}".format(game.round)
			s.calculateDecision( self.getCurrentHistory(game), verb )
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

	def updateState(self, game):
		# add current decision to the agents history
		self.dHistory.append((game.round, self.decision))
		# update the score, if agent won +1 or -1 if lost
		# correctDecision = 1 if ( game.attendance[-1][1] <= (len(game.agents)/2) ) else 0
		if self.decision == game.correctDecision:
			self.score.append(self.score[-1] + 1)
		else:
			self.score.append(self.score[-1] - 1)
		# update all the strategy scores
		for s in self.strats:
			s.updateState(game.round, game.correctDecision)

		if(self.verbose):
			self.writeLog(game)

	def writeLog(self, game):
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

''' Producer Agent
	Use in a MG to simulate markets, it always participates
	in the game with only one strategy, increasing thus the information
	in the model for speculators to use
'''
class ProducerAgent(ClassicAgent):
	def __init__(self, brainSize):
		# producer is just a classical agent with 1 strategy...
		ClassicAgent.__init__(self, brainSize, 1)
		self.type = "producer"

''' Speculator Agent
	Use in a MG to simulate markets, it participates
	in the game with only multiple strategies,
	but only when it has a strategy that will give him
	benefit.
'''

class SpeculatorAgent(ClassicAgent):
	def __init__(self, brainSize, nStrats, epsilon):
		ClassicAgent.__init__(self, brainSize, nStrats)
		self.type = "speculator"
		self.epsilon = epsilon
		# zero strategy is appended to the list of already existing strategies
		self.strats.append( strategy.ZeroStrat( self.brainSize, self.epsilon ) )

	# almost identical to the Classic Agent method
	# difference is that Speculator can abstain from participating
	# maintaining its score same if it is not profitable for him (zero strategy wins)
	def updateState(self, game):
		# add current decision to the agents history
		self.dHistory.append((game.round, self.decision))
		# update the score, if agent won +1 or -1 if lost
		# correctDecision = 1 if ( game.attendance[-1][1] <= (len(game.agents)/2) ) else 0
		if self.decision == game.correctDecision:
			self.score.append(self.score[-1] + 1)
		elif self.decision == None:
			# zero strategy won, just repeat the score
			self.score.append(self.score[-1])
		else:
			self.score.append(self.score[-1] - 1)
		# update all the strategy scores
		for s in self.strats:
			s.updateState(game.round, game.correctDecision)

class CAgent(ClassicAgent):
	def __init__(self, brainSize, nStrats):
		ClassicAgent.__init__(self, brainSize, nStrats)
		self.type = 'community'
		self.asd = 'asd'

	def generateStrats(self):
		for i in range(self.nStrats):
			# the generated strategy for Community Agent is 2*brainSize
			# because we have to take into account the local and global history
			self.strats.append( strategy.ClassicStrat( self.brainSize * 2 ) )

		log.info("Strategies generated: ")
		log.info(self.strats)

	def setCGame(self, cgame):
		self.cgame = cgame

	def getCurrentHistory(self, game):
		if (self.cgame):
			fromIdx = len(game.history) - self.brainSize
			fromCIdx = len(self.cgame.history) - self.brainSize
			newHist = self.cgame.history[fromCIdx:] + game.history[fromIdx:]
			if self.verbose: print newHist
			return newHist
		else:
			log.debug("No CGame in CAgent instance!")
			return False

	def updateState(self, game):
		# ClassicAgent.updateState(self, game)
				# add current decision to the agents history
		self.dHistory.append((game.round, self.decision))
		# update the score, if agent won +1 or -1 if lost
		# correctDecision = 1 if ( game.attendance[-1][1] <= (len(game.agents)/2) ) else 0
		if self.decision == game.correctDecision:
			self.score.append(self.score[-1] + 1)
		else:
			self.score.append(self.score[-1] - 1)
		# update all the strategy scores
		for s in self.strats:
			s.updateState(game.round, game.correctDecision)

		if(self.verbose):
			self.writeLog(game)

	def writeLog(self, game):
		f = open('../agent', 'a')
		f.write("Round number: {}\n".format(game.round))
		f.write("Global history: {}\n".format(game.history[len(game.history)-self.brainSize:]))
		f.write("Local history: {}\n".format(self.cgame.history[len(self.cgame.history)-self.brainSize:]))
		f.write("Decision made: {}\n".format(self.decision))
		for s in self.strats:
			f.write("Strategy: {}\n".format(s.strat))
			f.write("Strategy score: {}\n".format(s.getVScore()))
			f.write("Strategy decision: {}\n".format(s.decision))
			f.write("----------------------------------------\n")

		f.write("____________________________________________\n")


class IntelligentAgent(ClassicAgent):
	def __init__(self, brainSize, learningRate):
		Agent.__init__(self, "intelligent")
		self.brainSize = brainSize
		self.learningRate = learningRate
		# decision and history
		self.decision = 0
		# dHistory is a list of tuple (roundNumber, agentDecision)
		self.dHistory = []
		# strategy
		self.strategy = self.generateStrategy()

	def generateStrategy(self):
		return strategy.IntelligentStrat(self.brainSize, self.learningRate)

	def makeDecision(self, game):
		self.strategy.calculateDecision( self.getCurrentHistory(game) )
		self.decision = self.strategy.getDecision()

	def updateState(self, game):
		# add current decision to the agents history
		self.dHistory.append((game.round, self.decision))
		# update the score, if agent won +1 or -1 if lost
		# correctDecision = 1 if ( game.attendance[-1][1] <= (len(game.agents)/2) ) else 0
		if self.decision == game.correctDecision:
			self.score.append(self.score[-1] + 1)
		else:
			self.score.append(self.score[-1] - 1)
		# update all the strategy scores
		self.strategy.updateState(game.round, game.correctDecision)
