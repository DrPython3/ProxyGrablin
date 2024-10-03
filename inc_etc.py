# -*- coding: utf-8 -*-

__title__ = "ETC for ProxyGrablin"
__description__ = "Various basic functions for project 'ProxyGrablin'."
__author__ = "DrPython3"
__date__ = "2024-10-03"
__version__ = "0.1"
__contact__ = "https://github.com/DrPython3"

# Needed modules:
import sys
import os
from datetime import datetime

# Functions:
def logging(text):
	"""
	Saves logs to a textfile.
	:param str text: log to write
	:return: True (saved), False (not saved)
	"""
	output_file = str("logs.txt")
	timestamp = datetime.now()
	logtime = str(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
	try:
		os.makedirs("logs")
	except:
		pass
	try:
		logfile = str(os.path.join("logs", str(f"{output_file}")))
		with open(logfile, "a+") as target_file:
			target_file.write(f"{logtime} | {text}\n")
		return True
	except:
		return False

def writer(output, output_file):
	"""
	Saves a given output to a text file.
	:param output: output to write (list)
	:param output_file: file to store the output
	:return: None
	"""
	try:
		with open(output_file, "w") as file:
			for item in output:
				file.write(item + "\n")
	except:
		pass

# DrPython3 (C) 2024
