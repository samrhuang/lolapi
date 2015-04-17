#!/usr/bin/env python

# Short script to anonymize time points for display purposes.  Input is a csv
# file with three columns: champion name, histogram value, time value.  Time
# values are sorted to ensure proper order and then given anonymous integer
# values starting from 0.  Distance between time points is NOT preserved (i.e.
# t=6, t=9, t=200 will map to t=0, t=1, t=2).

import fileinput

def anonymize_times():
  #print "Heya!"

  input_file = fileinput.input()

  # Skip the header line
  header = input_file.readline().strip()

  data = list()
  anonymized_data = list()
  dates = dict()
  counter = 0

  for line in input_file:
    original_line = line.strip().split(',')
    data.append(original_line)

  date_func = lambda x: long(x[-1])
  sort_func = lambda x, y: cmp(date_func(x), date_func(y))

  sorted_data = sorted(data, sort_func)

  for d in sorted_data:
    if date_func(d) not in dates:
      dates[date_func(d)] = counter
      counter += 1

    anon_d = d[0:-1]
    anon_d.append(str(dates[date_func(d)]))

    anonymized_data.append(','.join(anon_d))


  print header
  for ad in anonymized_data:
    print ad



def main():
  anonymize_times()

if __name__ == "__main__":
  main()
