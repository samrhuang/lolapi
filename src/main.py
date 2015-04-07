#!/usr/bin/env python


import calendar
import time

import lol_api_calls
import our_utils
import lol_scraper

def get_api_key():
  api_key_file = "api_key"

  # Get the api key to use
  f = open(api_key_file, 'r')
  api_key = f.read().strip()
  f.close()

  return api_key

def test_calls():

  # Set region to use
  region = "na"

  #lol_api_root = "https://na.api.pvp.net/api/lol/" + region

  api_key = get_api_key()

  epoch_time = calendar.timegm(time.gmtime())
  # Adjust epoch time to be a multiple of 5 minutes, or 300 seconds by rounding
  # down to the most recent multiple.
  #
  # NOTE: From trial and error, it seems that the most recent multiple is not
  # good, because the 5-period block must be completed in order for the query
  # to behave.  So take the block prior.
  adjusted_epoch_time = ((epoch_time/300)-1)*300

  # FIXME Hacked in for testing purposes, remove for additional testing
  adjusted_epoch_time = 1428206100
  print adjusted_epoch_time, time.gmtime(adjusted_epoch_time)

  game_ids = lol_api_calls.api_challenge_game_ids(region, api_key, adjusted_epoch_time)
  print game_ids

  # For each game in list, process stats for it
  for game_id in game_ids:
    print game_id
    process_game_stats(region, api_key, game_id)

def process_game_stats(region, api_key, game_id):
  summary = lol_api_calls.get_match(region, api_key, game_id)
  print our_utils.json_pretty_print(summary)

def scrape_data(region, api_key):
  lol_scraper.scrape_all_games(region, api_key, "scraped_data-Apr2_part2")



def main():

  #test_calls()

  api_key = get_api_key()

  scrape_data("na", api_key)

if __name__ == "__main__":
  main()
