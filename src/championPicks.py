#!/usr/bin/env python

# Script to produce histograms of champion picks for each timestamp (epoch).  A
# histogram is built for each timestamp over all games registered by that
# timestamp.  Histograms are stored as json in the same directory as the match
# data being scanned.
#
# We assume data has been generated using scrapeMatches.py.  This means that
# the scraped directory being scanned by this script has the following structure:
# 
# directory head
#   -> a .cfg file produced by scrapeMatches.py
#   -> a directory for each epoch that was scraped, labeled as the timestamp
#     -> a .log showing the query run to get match ids for this epoch and the
#        query result
#     -> an output file with the saved query result in json format
#     -> a directory for each game id the query returned
#        -> a .log showing the query run to get the match summary for this
#           match and the result
#        -> an output file with the saved query result in json format

import ConfigParser
import os
import sys
import json

import our_utils

def usage():
  print "Usage: " + sys.argv[0] + " <champion picks config file>"

def initialize_champion_dictionary(config):
  champDict = dict()

  champFile = open(config.get("OnlineSettings", "originalDirectory") + os.sep + config.get("Files", "dataDirectory") + os.sep + "lol-static-data" + os.sep + "champion" + os.sep + config.get("Files", "prettyOutputName"), "r")
  champData = json.load(champFile)
  champFile.close()

  for id in champData.get("keys").keys():
    champDict[int(id)] = [0, str(champData.get("keys")[id]) ]

  return champDict

def create_champion_pick_histograms(config):

  this_dir = os.getcwd()
  #print ">>>", config.get("Files", "scrapedDirectory")
  os.chdir(config.get("Files", "scrapedDirectory"))
  scan_one_day(config)
  os.chdir(this_dir)

def scan_one_day(config):
  scrapedConfig = ConfigParser.SafeConfigParser()
  scrapedConfig.read(config.get("Files", "scrapeConfigFile"))

  our_utils.config_dump(config, scrapedConfig)


  start_epoch = long(scrapedConfig.get("Time Ranges", "startEpoch"))
  end_epoch = long(scrapedConfig.get("Time Ranges", "endEpoch"))

  start_dir = os.getcwd()
  for t in range(start_epoch, end_epoch, 300):
    # Add data from match data
    print "Aggregating data from epoch", t

    os.chdir(str(t))
    scan_one_epoch(scrapedConfig, t)
    os.chdir(start_dir)

def scan_one_epoch(config, epoch):
  f = open(config.get("Files", "prettyOutputName"), "r")
  game_ids = json.loads(f.read())
  f.close()

  champion_counts = initialize_champion_dictionary(config)

  # Go through each game recorded in this epoch
  start_dir = os.getcwd()
  for game_id in game_ids:
    os.chdir(str(game_id))
    scan_one_match(config, champion_counts)
    os.chdir(start_dir)

  f = open(config.get("Files", "championPickHistogram"), "w")
  f.write(our_utils.json_pretty_print(champion_counts))
  f.close()

def scan_one_match(config, running_counts):

  f = open(config.get("Files", "prettyOutputName"), "r")
  match_detail = json.load(f)
  f.close()

  participants = match_detail.get("participants")

  for p in participants:
    champID = p.get("championId")
    running_counts[champID][0]+=1


def main():
  if len(sys.argv) < 2:
    usage()
    return

  championPicksConfigFile = sys.argv[1]

  config = ConfigParser.SafeConfigParser()
  config.read(championPicksConfigFile)


  starting_dir = os.getcwd()

  config.add_section("OnlineSettings")
  config.set("OnlineSettings", "originalDirectory", starting_dir)

  create_champion_pick_histograms(config)
  os.chdir(starting_dir)

  #sum = 0
  #for k in champion_pick_counts.keys():
    #sum += champion_pick_counts[k][0]

  #print sum

  #sorted_list = sorted(champion_pick_counts.values(), lambda x,y: cmp(x[0], y[0]))
  #for x in sorted_list:
    #print x

if __name__ == "__main__":
  main()
