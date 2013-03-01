#!/usr/bin/env python
# <config>
# Number of seconds to report after
REPORT_TIME = 1*60
COSM_API_KEY = ""
FEED_ID = 116173

# </config><code>
import serial, string, time, requests

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

last_sent = 0
while 1:
	line = ser.readline().strip()
	if not line:
		time.sleep(1)
		continue

	vals = line.split(" ")
	if len(vals) > 4:
		temperature = vals[1]
		humidity = vals[3]
		print "Current temperature: "+str(temperature)+"C Humidity: "+str(humidity)+"%"
		if (time.time() - last_sent) > REPORT_TIME:
			print "Reporting."
			vals = "1,"+str(temperature)+"\n"
			vals += "2,"+str(humidity)+"\n"
			header = {"X-ApiKey": COSM_API_KEY}
			r = requests.put('http://api.cosm.com/v2/feeds/'+str(FEED_ID)+".csv", headers=header, data=vals)
			print r.status_code
			last_sent = time.time()
