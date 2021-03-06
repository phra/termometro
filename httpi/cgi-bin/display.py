#!/usr/bin/python

import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep             # lets us have a delay
import mosquitto
import os
import time
import sys
import subprocess

# I'm using a Quick2Wire I/O board
# p1 == blue LED
# p2 == red LED
# p3 == green LED

#bpin = 18
#rpin = 27
#gpin = 22

GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
#GPIO.setup(bpin, GPIO.OUT)           # set blue pin as an output
#GPIO.setup(rpin, GPIO.OUT)           # set red pin as an output
#GPIO.setup(gpin, GPIO.OUT)           # set green pin as an output

def on_message(mqtts, msg):

	#if (str(msg.payload) == "b'BLUE'"
    #    or str(msg.payload) == "b'CYAN'"
    #    or str(msg.payload) == "b'MAGENTA'"
    #    or str(msg.payload) == "b'WHITE'"):
	#	GPIO.output(bpin, 1)         # set blue pin to 1/GPIO.HIGH/True
	#else:
	#	GPIO.output(bpin, 0)         # set blue pin to 0/GPIO.LOW/False
    str2display(str(msg.payload))

def str2display(s):
    subprocess.check_output(["./hd44780.py", s, "test"])


def temp2display():
    output = subprocess.check_output(["./Adafruit_DHT", "22", "4"])
     #print output
    matches = re.search("Temp =\s+([0-9.]+)", output)
    if (not matches):
        sys.exit(0)
    temp = float(matches.group(1))
    # search for humidity printout
    matches = re.search("Hum =\s+([0-9.]+)", output)
    if (not matches):
        sys.exit(0)
    humidity = float(matches.group(1))
    #print "Temperature: %.1f C" % temp
    #print "Humidity:    %.1f %%" % humidity
    subprocess.check_output(["./hd44780.py", "Temperatura %.1f" % temp, "Umidita' %.1f" % humidity])


# DEBUGGING Code
#	print ("Message received on topic: "+msg.topic+
#	"... with QoS: "+str(msg.qos)+
#	"... and payload: "+str(msg.payload))

def main():

	broker = "127.0.0.1"
	port = 1883

	mypid = os.getpid()
	sub_uniq = "subclient_"+str(mypid)
	mqtts = mosquitto.Mosquitto(sub_uniq)
	mqtts.on_message = on_message

	mqtts.connect(broker, port, 60)
	mqtts.subscribe("test/pi/display", 0)

	try:
		rc = 0
		while rc == 0:
			rc = mqtts.loop()
		GPIO.cleanup()
		return 0

	except KeyboardInterrupt:   # trap a CTRL+C keyboard interrupt
		GPIO.cleanup()      # resets all GPIO ports used by this program
		return 4

if __name__ == "__main__":
	sys.exit(main())
