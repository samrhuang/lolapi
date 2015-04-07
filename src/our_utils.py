#!/usr/bin/env python

import json

def json_pretty_print(j):
  return json.dumps(j, sort_keys = True, indent = 2, separators = (",", ":"))

# Basic logging class for use with our stuff
class Logger:
  logfile = None

  def __init__(self, logName):
    # TODO: Maybe add checking to see if file exists before opening
    self.logfile = open(logName, "w")

  def writeLog(self, msg):
    self.logfile.write(msg)

  def closeLog(self):
    self.logfile.close()
