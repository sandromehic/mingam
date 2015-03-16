import random

def randomDecision():
	random.seed()
	desc = random.randrange(0,2)
	if (desc==0):
		desc = -1
	return desc
