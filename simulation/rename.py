import os

dirname = '../data/2015-04-15 23:48:42.795263_/'
files = os.listdir(dirname)
for f in files:
	print f
	asd = f.split('_')
	# print asd
	asd.remove('')
	# print asd
	asd = '_'.join(asd)
	# print asd
	os.rename(dirname+f,dirname+asd)