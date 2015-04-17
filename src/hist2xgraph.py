#!/usr/bin/env python

import json
import sys

def usage():
  print "Usage: " + sys.argv[0] + " <histogram file> <key file>"

def main():
  if len(sys.argv) < 3:
    usage()
    return

  histogram_file = sys.argv[1]
  key_file_name = sys.argv[2]
  f = open(histogram_file, "r")
  hist = json.load(f)
  f.close()


  data = hist.items()
  cmp_func = lambda x, y: cmp(x[1][1], y[1][1])
  sorted_data = sorted(data, cmp_func)



  key_file = open(key_file_name, "w")
  for q in range(len(sorted_data)):
    print q, sorted_data[q][1][0]
    key_file.write(str(q)+ " "+ sorted_data[q][1][1] + "\n")

  key_file.close()



if __name__ == "__main__":
  main()
