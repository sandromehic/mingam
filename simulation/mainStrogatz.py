import logging as log
import argparse
from utils import *
import game
from itertools import product
import datetime

''' parse input arguments
	mainly for verbose option
	and use log to output info to screen for debugging
'''
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose mode turned on!")


'''
usage to addAgents, pass a tuple as arguments

to add classical agents call Game method addAgents like this
gameInstance.addAgents('classic', numberOfAgents, brainSize, numberOfStrategies)

to add producers (agents with only one strategy and always active) call this
gameInstance.addAgents('producer', numberOfAgents, brainSize, 1)

to add speculators (agents with S strategies and a Zero Strategy that prevents
them from participating in the market if their virtual score are not high enough,
epsilon is the controll parameter, usually 0.01 or 0.1)
gameInstance.addAgents('speculator', numberOfAgents, brainSize, numberOfStrategies, epsilon)
'''

# boltzmann folder
saveDirname = generateFolderName('data/', '')
# saveDirname = generateFolderName('../data/', '')

betas = [0.05, 0.1, 0.25, 0.5]

for run in range(runs):
	for brainSize in M:
		for nOfAgents in N:
			for beta in betas:
				neighSize = generateNeighSize(nOfAgents)
				neighSize = neighSize[:25]
				# neighSize.append(nOfAgents)
				print nOfAgents, neighSize
				for nOfNeigh in neighSize:
					i+=1
					# g, cgs = generateFixedGameComunities(nOfAgents, brainSize, S, nOfNeigh)
					g, cgs = generateWattsStrogatzGame(nOfAgents, brainSize, S, nOfNeigh, beta)

					print "{} - Starting the Game {} of total: {}, number of cgames: {}".format(datetime.datetime.now(), i, totalGames, len(cgs))
					runComunityRound(g, cgs, nRounds)

					(gameName, agentsName, scoreName) = getSaveNamesCommunity('game_'+str(i), nOfAgents, nOfNeigh, run, brainSize)
					comunityName = getComunitySaveName('game_'+str(i), nOfAgents, nOfNeigh, run, brainSize)
					g.saveResults(gameName, saveDirname)
					g.saveNumberOfComunities(comunityName, saveDirname)
