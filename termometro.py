#!/usr/bin/python
import time
import os
import sys
import subprocess
import re

# Run the DHT program to get the humidity and temperature readings!
output = subprocess.check_output(["./Adafruit_DHT", "22", "4"]);
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

print "Temperature: %.1f C" % temp
print "Humidity:    %.1f %%" % humidity

subprocess.check_output(["./hd44780.py", "Temperatura %.1f" % temp, "Umidita' %.1f" % humidity]);
