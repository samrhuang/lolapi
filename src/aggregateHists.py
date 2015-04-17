#!/usr/bin/env python

# Script to perform histogram aggregation.  We basically are adding
# distributions.  No smoothing is performed (as of now!).

import sys
import json
import our_utils
import ConfigParser
import os

def usage():
  print "Usage: " + sys.argv[0] + " <conf file>"

def read_hist_from_file(filename):
  f = open(filename, "r")
  hist = json.loads(f.read())
  return hist

def incorporate_hist(running_hist, new_hist):
  for k in new_hist.keys():
    if k not in running_hist:
      running_hist[k] = [0, new_hist[k][1]]
    running_hist[k][0] += new_hist[k][0]

def main2():
  if len(sys.argv) < 2:
    usage()
    return

  running_hist = dict()
  for q in range(1, len(sys.argv)):
    hist = read_hist_from_file(sys.argv[q])
    incorporate_hist(running_hist, hist)

  print our_utils.json_pretty_print(running_hist)

def aggregate_histograms(config):
  startEpoch = long(config.get("Time Ranges", "startEpoch"))
  endEpoch = long(config.get("Time Ranges", "endEpoch"))
  numDivisions = int(config.get("Time Ranges", "numDivisions"))

  epochIncrement = 300

  # Automatic flooring due to no floating precision
  numRawHists = (endEpoch - startEpoch)/epochIncrement + 1

  if numRawHists % numDivisions != 0:
    msg = "The number of divisions specified (%d) must evenly divide the raw number of valid epochs (%d) in the specified range (%ld, %ld)" % (numDivisions, numRawHists, startEpoch, endEpoch)
    raise Exception(msg)

  numEpochsPerDivision = numRawHists/numDivisions

  #print startEpoch, endEpoch, numDivisions
  #print numRawHists, numEpochsPerDivision

  # For each division, create a new histogram that aggregates all histograms of
  # epochs falling inside that division
  for div in range(numDivisions):

    running_hist = dict()
    for q in range(numEpochsPerDivision):
      curEpoch = startEpoch + (div*numEpochsPerDivision + q) * epochIncrement
      #print curEpoch
      hist = read_hist_from_file(config.get("Files", "dataScrapeRoot") + os.sep + str(curEpoch) + os.sep + config.get("Files", "rawHistFilenames"))
      incorporate_hist(running_hist, hist)

    # Write the finished running hist to file
    f = open(config.get("Files", "aggHistFileStem") + str(div) + ".hist", "w")
    f.write(our_utils.json_pretty_print(running_hist))
    f.close()


def main():
  if len(sys.argv) < 2:
    usage()
    return

  aggregateHistConfigFile = sys.argv[1]

  config = ConfigParser.ConfigParser()
  config.read(aggregateHistConfigFile)

  aggregate_histograms(config)


if __name__ == "__main__":
  main()
