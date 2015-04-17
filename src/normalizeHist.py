#!/usr/bin/env python

import json
import sys

import our_utils

def usage():
  print "Usage: " + sys.argv[0] + " <hist file>"

def main():
  if len(sys.argv) < 2:
    usage()
    return

  histogram_file = sys.argv[1]
  f = open(histogram_file, "r")
  hist = json.load(f)
  f.close()

  total = 0
  for k in hist:
    total += hist[k][0]

  for k in hist:
    hist[k][0] /= float(total)

  print our_utils.json_pretty_print(hist)


if __name__ == "__main__":
  main()
