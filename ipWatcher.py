import requests # for http requests
import time 	# for UTC time and sleep
import datetime # for date / time formatting

logFile = open("ipLog.csv", "a+") # creates the log file if doesnt already exist
logFile.close()

fileEmpty = False
logFile = open("ipLog.csv", "r+")
print(len(logFile.readlines()))
if len(logFile.readlines()) == 0:
	fileEmpty = True	
logFile.close()

# TODO: BUG: Always prints data,ip when program is started, should only print if file is empty
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
		print(lastLine)

	# if IP has changed, log new IP
	oldIp = lastLine.split(",")[1] + '\n'
	if oldIp != ip:
		print(f"oldIp: {oldIp} ip: {ip}")
		with open("ipLog.csv", "a+") as ipLog:
			timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			ipLog.write(timeStamp + "," + ip + '\n')
	time.sleep(5)
