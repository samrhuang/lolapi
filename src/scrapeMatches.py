#!/usr/bin/env python


import calendar
import time
import ConfigParser
import sys

import lol_scraper

def usage():
  print "Usage: " + sys.argv[0] + " <configFile>"

def get_api_key(config):
  api_key_file = config.get("Files", "apiKeyFile")

  # Get the api key to use
  f = open(api_key_file, 'r')
  api_key = f.read().strip()
  f.close()

  return api_key

def scrape_data(config, region, api_key):
  lol_scraper.scrape_all_games(config, region, api_key)



def main():

  if len(sys.argv) < 2:
    usage()
    return

  scraperConfigFile = sys.argv[1]
  

  # Read in configuration settings
  config = ConfigParser.ConfigParser()
  config.read(scraperConfigFile)

  config.add_section("OnlineSettings")
  config.set("OnlineSettings", "scraperConfigFile", scraperConfigFile)

  api_key = get_api_key(config)

  scrape_data(config, "na", api_key)

if __name__ == "__main__":
  main()
