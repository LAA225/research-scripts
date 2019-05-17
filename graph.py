import matplotlib.pyplot as plt
import sys
import matplotlib.ticker as tic

database = {}

def seconds(time):
	#print(time)
	t = time.split(':')
	t = list(map(lambda x: int(x), t))
	return t[0]*60*60 + t[1]*60 + t[2]

def data(filenames):
	for file in filenames:
		with open(file, 'r') as f:
			lines = f.readlines()
			lines = lines[1:]
			
			kcpu = []
			lcpu = []
			time = []
			kcpu_num = []
			lcpu_num = []
			for each in lines:
				splitLine = each.split()
				kcpu.append(float(splitLine[0])*100)
				lcpu.append(float(splitLine[1])*100)
				time.append(seconds(splitLine[2]))
				kcpu_num.append(int(splitLine[3]))
				lcpu_num.append(int(splitLine[4]))
				

			name = file[:-4]
			database[file] = {'kswapd' : kcpu,'gmail' : lcpu, 'time' : time, 'name': name, 'kcpu_num': kcpu_num, 'lcpu_num': lcpu_num }

def normalizeTime(run, start):
	#start = seconds(start)
	startingTime = run[0]

	x = 0
	while(startingTime != start):
		x += 1
		startingTime = run[x]

	timings = []
	for each in range(x,len(run)):
		time = run[each]
		timings.append(time - startingTime)

	return timings

def plot():
	fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
	ax0 = ax[0]
	ax1 = ax[1]
	ax = [ax0,ax1]
	for i,each in enumerate(database):
		print(each)
		#if want to coordinate with pss
		#starting = input('starting time: ')
		starting = database[each]['time'][0]
		x = normalizeTime(database[each]['time'], starting)
		cut = len(database[each]['time']) - len(x)
		y = database[each]['kswapd'][cut:]

		# x = x[10:]
		# y = y[10:]
		ax[i].plot(x,y, label = database[each]['name'] + 'KB')
		ax[i].set_xlim([0,600])

		ax[i].set_xlabel('time / s', fontsize = 16)
		ax[i].set_ylabel('cpu utilization / %', fontsize = 16)
		#plt.title('change in PSS with differnt lmkd thresholds')
		#plt.legend(loc = 1)
		ax[i].xaxis.set_tick_params(labelsize=12)
		ax[i].yaxis.set_tick_params(labelsize=12)
		
		#plt.savefig('kswapd.jpg')
		ax[i].legend(loc = 1, fontsize = 12)
	plt.show()

def cpu():
	fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
	ax0 = ax[0]
	ax1 = ax[1]
	ax = [ax0,ax1]
	for i,each in enumerate(database):
		print(each)
		starting = input('starting time: ')
		x = normalizeTime(database[each]['time'], starting)
		cut = len(database[each]['time']) - len(x)
		y = database[each]['cpu_num'][cut:]


		# x = x[10:]
		# y = y[10:]
		ax[i].plot(x,y, label = database[each]['name'] + 'KB')
		ax[i].set_yscale('linear')

		ax[i].set_xlabel('time / s')
		ax[i].set_ylabel('cpu')
		#plt.title('change in PSS with differnt lmkd thresholds')
		#plt.legend(loc = 1)
		
		#plt.savefig('kswapd.jpg')
		ax[i].legend(loc = 1)
	plt.show()

def together():
	# fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
	# ax0 = ax[0]
	# ax1 = ax[1]
	# ax = [ax0,ax1]
	for i,each in enumerate(database):
		print(each)
		starting = input('starting time: ')
		x = normalizeTime(database[each]['time'], starting)
		cut = len(database[each]['time']) - len(x)
		y = database[each]['kswapd'][cut:]

		fig, ax = plt.subplots(nrows=2, ncols=1)
		ax0 = ax[0]
		ax1 = ax[1]
		ax = [ax0,ax1]
		# x = x[10:]
		# y = y[10:]
		ax[0].plot(x,y, label = database[each]['name'] + 'KB')
		#ax[i].set_ylim([0,7])

		ax[0].set_xlabel('time / s', fontsize = 16)
		ax[0].set_ylabel('cpu utilization / %', fontsize = 16)
		ax[0].xaxis.set_tick_params(labelsize=16)
		ax[0].yaxis.set_tick_params(labelsize=16)
		ax[0].legend(loc = 1)

		y1 = database[each]['cpu_num'][cut:]
		ax[1].plot(x,y1, label = database[each]['name'] + 'KB')
		temp = tic.MaxNLocator(4)
		ax[1].yaxis.set_major_locator(temp)

		ax[1].set_xlabel('time / s', fontsize = 16)
		ax[1].set_ylabel('cpu', fontsize = 16)
		
		ax[1].xaxis.set_tick_params(labelsize=16)
		ax[1].yaxis.set_tick_params(labelsize=16)

		plt.tight_layout()
		
		ax[1].legend(loc = 1)

		plt.show()


def main():
	if(len(sys.argv) < 2):
		print('give name of data file as well')
	else:
		data(sys.argv[1:])
		plot()
		#cpu()
		# together()

if __name__ == '__main__':
	main()