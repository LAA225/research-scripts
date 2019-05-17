import subprocess 
import time
import csv
import sys
import os

processName = sys.argv[1]
fileExists = True
fileName = 'gmail0'
while(fileExists):
    if(os.path.isfile(fileName+'.csv')):
        value = int(fileName[5:])
        value = value + 1;
        fileName = fileName[:5]
        fileName = fileName+str(value)
        print(fileName)
    else:
        fileExists = False
fileName  = fileName+'.csv'
f = open(fileName,'w')
writer = csv.writer(f)
writer.writerow(['Time(s)','TOTAL PSS'])
currentTime = 0
startTime = round(time.time())
while(1):
    value = subprocess.run(["adb","shell","dumpsys","meminfo",processName,"|","grep","TOTAL"],capture_output=True)
    currentTime = round(time.time())
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(currentTime))
    ctime = currentTime.split()

    valueList = str(value.stdout).split()
    print(valueList[2])
    totalPSS = int(valueList[2])/ 1024
    writer.writerow([ctime[1],totalPSS])
    time.sleep(0.5)