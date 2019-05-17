import numpy as np
import sys
import matplotlib.pyplot as plt

database = {}
graph = 'cdf'

def isolate(lines,runs):
	run = []
	for x in range(1,len(lines)):
		r = lines[x].split(',')
		r[-1] = r[-1][:-1]
		#print(r)
		for x in range(1,len(r)):
			r[x] = float(r[x])
		run.append(r)

	return run

def read(file,runs):
	with open(file, 'r') as f:
			lines = f.readlines()
			
			previous = 0
			for x in range(len(lines)):
				if(lines[x][:4] == 'time' and previous < x):
					run = isolate(lines[previous:x],runs)
					previous = x
					
					runs.append(run)
					#print('************************************************************')

			run = isolate(lines[previous:],runs)
			runs.append(run)

def seconds(time):
	#print(time)
	t = time.split(':')
	t = list(map(lambda x: int(x), t))
	return t[0]*60*60 + t[1]*60 + t[2]


def getTimings(runs):
	timings = []
	for each in runs:
		startingTime = seconds(each[0][0])
		endingTime = 0
		for run in each:
			if run[2] == 0:
				endingTime = seconds(run[0])
				break

		timings.append(endingTime - startingTime)

	return timings

def getCrash(runs):
	crash = []
	for each in runs:
		crashMem = 0
		for run in each:
			if run[2] == 0:
				crashMem = run[1]
				break
		crash.append(crashMem)

	return crash



def makeCDF(filenames,graph):
	for file in filenames:
		runs = []
		read(file,runs)
		totalTimes = getTimings(runs)
		crashMem = getCrash(runs)
		database[file] = {'filename':file[:-3],'runs': runs, 'timesToCrash' : totalTimes, 'crashMem': crashMem}

	if(graph == 0):
		for each in database:
			print(database[each]['timesToCrash'])
			# print(database[each]['crashMem'])
			
			x = np.sort(database[each]['timesToCrash'])
			y = np.arange(1,len(x)+1) / len(x)
			y = y * 100
			
			plt.plot(x,y,label = database[each]['filename'] + 'MB')
			plt.xlim([350,600])
			
			plt.xlabel('time to crash / s')
			plt.ylabel('CDF')
			#plt.title('Time to crash with different lmkd thresholds')
			plt.legend(loc = 1)

			plt.savefig('cdf.jpg')


def normalizeTime(run):
	startingTime = seconds(run[0][0])
	timings = []
	for each in run:
		time = seconds(each[0])
		timings.append(time - startingTime)

	return timings

def getPSS(run):
	PSS = []
	for each in run:
		PSS.append(each[2])

	return PSS

def PSSgraph():
	for each in database:
		print(each)
		x = normalizeTime(database[each]['runs'][0])
		y = getPSS(database[each]['runs'][0])

		x = x[10:]
		y = y[10:]
		plt.plot(x,y, label = database[each]['filename'] + 'MB')

		plt.xlabel('time / s')
		plt.ylabel('PSS / MB')
		#plt.title('change in PSS with differnt lmkd thresholds')
		plt.legend(loc = 1)

		plt.savefig('PSS.jpg')

def memoryGraph():
	for each in database:
		y0 = getActive(database[each]['runs'][0])
		y1 = getCache(database[each]['runs'][0])
		y2 = getFree(database[each]['runs'][0])
	# for each in database:
		# y0 = np.random.rand(100)
		# y1 = y0 + np.random.rand(100)
		# y2 = y1 + np.random.rand(100)
		# capacity = 3*np.ones(100)

		# # make the mpl plot (no fill yet)
		# fig, ax = plt.subplots()
		# ax.plot(y0, label='y0')
		# ax.plot(y1, label='y1')
		# ax.plot(y2, label='y2')
		# ax.plot(capacity, label='capacity')

		# # set all traces' "fill" so that it fills to the next 'y' trace
		# update = {'data':[{'fill': 'tonexty'}]}

		# # strip style just lets Plotly make the styling choices (e.g., colors)
		# plotly_fig = tls.mpl_to_plotly( fig )
		# plotly_fig.update(update)
		# py.iplot(plotly_fig, strip_style=True, filename='mpl-stacked-line')


def main():
	if(len(sys.argv) < 2):
		print('give the name of the file to open as well')
	else:
		graph = input('0 for cdf, 1 for PSS, 2 for memory: ')
		graph = int(graph)
		filenames = sys.argv[1:]
		
		makeCDF(filenames,graph)
	
		if(graph == 1):
			PSSgraph()

		if(graph == 2):
			memoryGraph()

if __name__ == '__main__':
	main()