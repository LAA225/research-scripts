import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import numpy as np

database = {}

timesFont = {'fontname': 'Times New Roman'}

def seconds(time):
	# print(time)
	t = time.split(':')
	t = list(map(lambda x: int(x), t))
	return t[0]*60*60 + t[1]*60 + t[2]


def data(filenames):
	for file in filenames:
		with open(file, 'r')as f:
			lines = f.readlines()

			time = []
			pss = []
			seperation = []
			for x in range(1,len(lines)):
				splitline = lines[x].split(',')
				# if file == 'gmail_go_app1.csv':
				# 	print(splitline)

				if(splitline[0] == ''):
					continue

				if(splitline[2] != '\n'):
					seperation.append(seconds(splitline[0]))

				time.append(seconds(splitline[0]))
				pss.append(int(float(splitline[1])))

			# if file == 'gmail_go_app1.csv':
			# 	print(seperation)
			name = ''
			if file == 'basic_gmail_browser.csv':
				name = 'Basic Gmail on Browser'
			elif file == 'standard_gmail_browser.csv':
				name = 'Standard Gmail on Browser'
			elif file == 'latest_gmail_app.csv':
				name = 'Gmail App'
			elif file == 'gmail_go_app.csv':
				name = 'Gmail Go App'
			elif file == 'older_gmail_app':
				name = 'what ever verion'

			database[file] = {'time': time, 'pss': pss, 'seperate': seperation, 'name':name}

def normalize(file):
	seperate = database[file]['seperate'][0]
	index = 0
	sTime = database[file]['time'][0]
	while(seperate > sTime):
		index +=1
		sTime = database[file]['time'][index]

	startingTime = database[file]['time'][0]
	database[file]['startingTime'] = startingTime

	database[file]['seperate'] = list(map(lambda x: x - startingTime, database[file]['seperate']))
	ans = list(map(lambda x: x-startingTime, database[file]['time']))
	return ans

def equal(standard):
	for each in database:
		cut = database[each]['seperate'][0] - standard
		database[each]['x'] = list(map(lambda x: x - cut , database[each]['x']))

		index = 0
		while(database[each]['x'][index] < 0):
			index += 1

		database[each]['x'] = database[each]['x'][index:]
		database[each]['y'] = database[each]['y'][index:]
		# database[each]['x'] = database[each]['x'][cut:]
		# start = database[each]['x'][0]
		# database[each]['x'] = list(map(lambda x: x - start, database[each]['x']))
		# database[each]['y'] = database[each]['y'][cut:]


def graph():
	for each in database:
		x = normalize(each)
		database[each]['x'] = x
		y = database[each]['pss']
		database[each]['y'] = y

	#pick one and draw the rest accordingly can't normalize each
	#one idea is to just pick the first. standardize it and then get the rest and make sure their 

	standarda = 500
	standardb = 500
	for each in database:
		print(database[each]['seperate'][0])
		if(database[each]['seperate'][0] < standarda):
			standarda = database[each]['seperate'][0]
			standardb = database[each]['seperate'][1]

	equal(standarda - 1)

	for each in database:
		if each == 'gmail_go_app1.csv':
			print(database[each]['y'])
		x = database[each]['x']
		y = database[each]['y']

		plt.plot(x,y, label = database[each]['name'])
		
		# if(each == 'older_gmail_app.csv'):
		plt.axvline(x = 30, linestyle = '-', color = 'k', linewidth = 0.75)
		plt.axvline(x = 60, linestyle = '-', color = 'k', linewidth = 0.75)
		plt.xlabel('Time (sec)', fontsize = 16)
		plt.ylabel('PSS (MB)', fontsize = 16)
		plt.xlim([0,90])
		plt.ylim([0,140])
		plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(30))
		#plt.title(' default page                        text email                                    image email               ')
		plt.text(15,130, 'Default view', horizontalalignment='center', verticalalignment='center', fontsize = 20, **timesFont)
		plt.text(45,130, 'Text email', horizontalalignment='center', verticalalignment='center', fontsize = 20, **timesFont)
		plt.text(75,130, 'Image email', horizontalalignment='center', verticalalignment='center', fontsize = 20, **timesFont)
		labelLineY = np.array([120 for i in range(95)])
		labelLinex = np.arange(95)
		plt.plot(labelLinex,labelLineY, color = 'k' , linewidth = 0.75)

		plt.legend(loc = 4, fontsize = 16)
		plt.gca().yaxis.grid(True)
		plt.gca().xaxis.set_tick_params(labelsize=16)
		plt.gca().yaxis.set_tick_params(labelsize=16)

		plt.tight_layout()

	plt.show()

def main():
	if(len(sys.argv) < 2):
		print("enter file names")
	else:
		data(sys.argv[1:])
		graph()

if __name__ == '__main__':
	main()