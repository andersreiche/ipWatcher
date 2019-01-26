import requests # for http requests
import time 	# for UTC time and sleep
import datetime # for date / time formatting
import subprocess # for linux notifications

def sendMessage(message):
    subprocess.Popen(['notify-send', message])
    return

# creates the log file if doesnt already exist
logFile = open("ipLog.csv", "a+") 
logFile.close()

# checks if the ipLog is empty
fileEmpty = False
logFile = open("ipLog.csv", "r+")
numLines = len(logFile.readlines())
if numLines == 0:
	print("File was Empty")
	fileEmpty = True	
logFile.close()

# if the IP log was empty, write the .csv header
if fileEmpty == True:
	with open("ipLog.csv", "a+") as ipLog:
		ipLog.write("date,ip\n")


while True:
	# gets IP address with an http GET request
	data = requests.get("http://httpbin.org/ip")

	# extracts body and make into string
	bodyString = str(data.content)

	# Splits bodyString into tokens with " as delimiter
	# then selects token on index 3 (ip address)
	ip = bodyString.split('"')[3]

	# check what IP was last time
	lastLine = ""
	with open("ipLog.csv", "r") as ipLog:
		lastLine = ipLog.readlines()[-1]

	# if IP has changed, log new IP
	oldIp = lastLine.split(",")[1]

	if oldIp != ip + '\n':
		with open("ipLog.csv", "a+") as ipLog:
			timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			ipLog.write(timeStamp + "," + ip + '\n')
			#print(f"{timeStamp} : IP changed")
			sendMessage("IP changed")
	time.sleep(60) # wait 1 minute


