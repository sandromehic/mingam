import logging as log
import agent
import numpy as np
import pandas as pd
 
class Game:
	def __init__(self):
		log.info("Starting the Game class")
		self.agents = []
		self.history = []
		self.attendance = []
		self.round = 0
		self.agSeries = {}
		self.rounds = {}

	def __str__(self):
		return "Inside Game Class"

	def addAgents(self, *args):

		if(args[0] == 'classic'):
			# args[1] = numberOfAgents
			# args[2] = brainSize
			# args[3] = numberOfStrategies
			for i in range(args[1]):
				self.agents.append( agent.ClassicAgent(args[2], args[3]) )
				# self.agSeries[self.agents[i].id] = []
				# self.agSeries.append( pd.Series([], name=self.agents[i].id) )

			for rnd in range(args[2]):
				np.random.seed
				self.history.append( np.random.randint(2) )

			log.info("Initial history: ")
			log.info(self.history)

	def runRound(self):
		# elaborate agent decisions
		att = []
		for (i, ag) in enumerate(self.agents):
			ag.makeDecision(self)
			# get agents decision and append it to attendance list
			agDecision = ag.getDecision()
			att.append(agDecision)
			# self.agSeries[self.agents[i].id].append(agDecision)

		# save attendance to the self.attendance list with the round number
		self.attendance.append((self.round, sum(att)))
		self.rounds[self.round] = att

		# update all agents states, that update their strategies
		correctDecision = 1 if ( self.attendance[-1][1] <= (len(self.agents)/2) ) else 0
		self.history.append(correctDecision)
		for ag in self.agents:
			ag.updateState(self)

		self.round += 1

	def runRounds(self, n):
		for i in range(n):
			self.runRound()

	def saveResults(self, filename, dirname):
		# out = pd.DataFrame(self.agSeries)
		out = pd.DataFrame(self.rounds)
		out.to_csv(dirname + filename)

	def saveHistory(self, filename, dirname):
		out = pd.DataFrame(self.history)
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

	def getAttendance(self):
		return self.attendance