#!/usr/bin/env python

import json
import sys

def usage():
  print "Usage: " + sys.argv[0] + " <histogram file> <epoch>"

def main():
  if len(sys.argv) < 3:
    usage()
    return

  histogram_file = sys.argv[1]
  epoch = sys.argv[2]
  f = open(histogram_file, "r")
  hist = json.load(f)
  f.close()

  for champID in hist.keys():
    print ",".join((str(hist[champID][1]), str(hist[champID][0]), epoch))

#print hist



if __name__ == "__main__":
  main()
