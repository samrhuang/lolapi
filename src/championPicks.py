#!/usr/bin/env python

import ConfigParser
import os
import sys
import json

import our_utils

def usage():
  print "Usage: " + sys.argv[0] + " <champion picks config file>"

def initialize_champion_dictionary():
  champDict = dict()

  champFile = open("lol-static-data/champion/output.pretty", "r")
  champData = json.load(champFile)
  champFile.close()

  for id in champData.get("keys").keys():
    champDict[int(id)] = [0, str(champData.get("keys")[id]) ]

  return champDict

def aggregate_champion_picks(config):
  champion_pick_counts = initialize_champion_dictionary()

  this_dir = os.getcwd()
  #print this_dir
  os.chdir("scraped_data-04_02")
  scan_one_day(config, champion_pick_counts)
  os.chdir(this_dir)

def scan_one_day(config, running_counts):
  scrapedConfig = ConfigParser.ConfigParser()
  scrapedConfig.read(config.get("Files", "scrapeConfigFile"))

  #print os.getcwd()
  #print scrapedConfig.sections()

  start_epoch = long(scrapedConfig.get("Time Ranges", "startEpoch"))
  end_epoch = long(scrapedConfig.get("Time Ranges", "endEpoch"))

  #print str(start_epoch) + " " + str(end_epoch)

  start_dir = os.getcwd()
  for t in range(start_epoch, end_epoch, 300):
    # Add data from match data
    print "Aggregating data from epoch ", t

    os.chdir(str(t))
    scan_one_epoch(config, running_counts, t)
    os.chdir(start_dir)
    break

def scan_one_epoch(config, running_counts, epoch):
  game_ids = [] # This should be the output from the lol api.  We forgot to store this for easy accesiblity.
  start_dir = os.getcwd()
  for game_id in game_ids:
    os.chdir(str(game_id))
    scan_one_match(config, running_counts)
    os.chdir(start_dir)

def scan_one_match(config, running_counts):
  data_dir = "data/scraped_data-04_02"

  f = open(data_dir + os.sep + "test" + os.sep + "1780429136" + os.sep + config.get("Files", "prettyOutputName"), "r")
  match_detail = json.load(f)
  f.close()

  #print match_detail
  #print our_utils.json_pretty_print(match_detail)

  #print "The match lasted " + str(match_detail.get("matchDuration")) 


  participants = match_detail.get("participants")

  for p in participants:
    #print "Participant ID " + str(p.get("participantId")) + " chose champion ID " + str(p.get("championId"))
    champID = p.get("championId")
    running_counts[champID][0]+=1


def main():
  if len(sys.argv) < 2:
    usage()
    return

  championPicksConfigFile = sys.argv[1]

  config = ConfigParser.ConfigParser()
  config.read(championPicksConfigFile)

  # NOTE: We assume the configuration file is in the root directory of the data
  # directory.
  #scraped_data_dir = sys.argv[1]
  #scraped_data_conffile = sys.argv[2]

  #config = ConfigParser.ConfigParser()
  #config.read(scraped_data_dir + os.sep + scraped_data_conffile)

  #print scraped_data_dir, scraped_data_conffile
  
  starting_dir = os.getcwd()

  os.chdir(config.get("Files", "dataDirectory"))
  aggregate_champion_picks(config)
  os.chdir(starting_dir)

if __name__ == "__main__":
  main()
