#!/usr/bin/env python

import json
import time

def json_pretty_print(j):
  return json.dumps(j, sort_keys = True, indent = 2, separators = (",", ":"))

# NOTE: I don't know of any existing way to dump all config options from one
# parser into another, so I wrote this to do it.
def config_dump(source_config_parser, dest_config_parser):
  for s in source_config_parser.sections():
    if not dest_config_parser.has_section(s):
      dest_config_parser.add_section(s)
    for [k, v] in source_config_parser.items(s):
      dest_config_parser.set(s, k, v)

# Basic logging class for use with our stuff
class Logger:
  logfile = None

  def __init__(self, logName):
    # TODO: Maybe add checking to see if file exists before opening
    self.logfile = open(logName, "w")

  def writeLog(self, msg):
    self.logfile.write(time.strftime("[%Y-%m-%d %H:%M:%S GMT] ", time.gmtime()) + msg)

  def closeLog(self):
    self.logfile.close()

