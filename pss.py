import matplotlib.pyplot as plt
import sys

database = {}

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
				print(splitline)
				if(splitline[0] == '' or splitline[0] == '\n'):
					continue

				time.append(seconds(splitline[0]))
				pss.append(int(float(splitline[1])))

			database[file] = {'time': time, 'pss': pss, 'seperate': seperation}

def normalize(time):
	start = time[0]
	ans = list(map(lambda x: x - start, time))

	return ans

def graph():
	for each in database:
		x = normalize(database[each]['time'])
		y = database[each]['pss']

		plt.plot(x,y, label = each[:-4] + 'KB')

		plt.xlabel('time / s', fontsize = 16)
		plt.ylabel('PSS / MB', fontsize = 16)
		plt.gca().xaxis.set_tick_params(labelsize=14)
		plt.gca().yaxis.set_tick_params(labelsize=14)
		plt.legend(loc = 1, fontsize = 14)

	plt.show()

def main():
	if(len(sys.argv) < 2):
		print("enter file names")
	else:
		data(sys.argv[1:])
		graph()

if __name__ == '__main__':
	main()