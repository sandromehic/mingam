import logging as log
import agent
import numpy as np
import pandas as pd

class Game:
	def __init__(self):
		log.info("Starting the Game class")
		self.agents = []
		self.history = []
		self.round = 0
		self.correctDecision = None
		self.rounds = {}

		self.generateRandomHistory()

	def __str__(self):
		return "Inside Game Class"

	def addAgents(self, *args):

		if(args[0] == 'classic'):
			# args[1] = numberOfAgents
			# args[2] = brainSize
			# args[3] = numberOfStrategies
			for i in range(args[1]):
				self.agents.append( agent.ClassicAgent(args[2], args[3]) )

		elif(args[0] == 'producer'):
			# args[1] = numberOfAgents
			# args[2] = brainSize
			for i in range(args[1]):
				self.agents.append( agent.ProducerAgent(args[2]) )

		elif(args[0] == 'speculator'):
			# args[1] = numberOfAgents
			# args[2] = brainSize
			# args[3] = numberOfStrategies
			# args[4] = epsilon (control parameter for zero strategy)
			for i in range(args[1]):
				self.agents.append( agent.SpeculatorAgent(args[2], args[3], args[4]) )
		elif(args[0] == 'community'):
			# args[1] = numberOfAgents
			# args[2] = brainSize
			# args[3] = numberOfStrategies
			for i in range(args[1]):
				self.agents.append( agent.CAgent(args[2], args[3]) )
		elif(args[0] == 'intelligent'):
			# args[1] = numberOfAgents
			# args[2] = brainSize
			# args[3] = learningRate
			for i in range(args[1]):
				self.agents.append( agent.IntelligentAgent(args[2], args[3]) )


	def generateRandomHistory(self):
		histRange = 16
		for rnd in range(histRange):
			np.random.seed
			self.history.append( np.random.randint(2) )

		log.info("Initial history: ")
		log.info(self.history)

	def runRound(self):
		# elaborate agent decisions
		att = []
		for (i, ag) in enumerate(self.agents):
			# get agents decision and append it to attendance list
			att.append( self.makeAgentsDecision(ag) )

		# save attendance to the self.attendance list with the round number
		# self.attendance.append((self.round, sum(att)))
		self.rounds[self.round] = att

		# update all agents states, that update their strategies
		# correctDecision = 1 if ( self.attendance[-1][1] <= (len(self.agents)/2) ) else 0
		self.calculateDecision()
		self.history.append(self.correctDecision)
		self.updateAgents()

		self.round += 1

	def runRounds(self, n):
		for i in range(n):
			self.runRound()

	def makeAgentsDecision(self, agent):
		# make the agents decision then return its result
		agent.makeDecision(self)
		return agent.getDecision()

	def updateAgents(self):
		for ag in self.agents:
			ag.updateState(self)

	def calculateDecision(self):
		log.debug('Calculating correct decision inside game class')
		att = []
		log.debug(att)
		for a in self.agents:
			# if agent participated at this round
			# else his decison is None and should
			# not be included in calculating attendance
			desc = a.getDecision()
			if (desc is not None): att.append(desc)

		log.debug(att)
		self.correctDecision = 1 if ( sum(att)<=len(att)/2 ) else 0
		log.debug(self.correctDecision)

	def saveResults(self, filename, dirname):
		out = pd.DataFrame(self.rounds)
		out.to_csv(dirname + filename)

	def saveAgentsScores(self, filename, dirname):
		out = {}
		for a in self.agents:
			name = str(a.type) + str(a.id)
			out[name] = a.score

		out = pd.DataFrame(out)
		out.to_csv(dirname + filename)

	def saveAgents(self, filename, dirname):
		f = open(dirname + filename, 'w')
		f.write("History: \n")
		f.write(str(self.history) + '\n')
		for ag in self.agents:
			f.write("Agent id: " + str(ag.id) + "\n")
			for (i, s) in enumerate(ag.strats):
				f.write("Strategy {} has virtual score {} \n".format(i, s.getVScore()))
				f.write(str(s.getStrat())  + '\n')

			f.write("----------------------\n")

class CGame(Game):
	def __init__(self):
		Game.__init__(self)

	def makeAgentsDecision(self, agent):
		return agent.getDecision()

	def updateAgents(self):
		pass
