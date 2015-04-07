import os
import json

import lol_api_calls as lac
import our_utils

def scrape_all_games(region, api_key, dump_directory):

  try:
    os.mkdir(dump_directory)
    os.chdir(dump_directory)
  except OSError as e:
    print "Dump directory already exists, exiting..."
    raise e


  # Start date is April 2nd, midnight, GMT.
  start_epoch = 1427932800

  # Set end epoch date to be April 5th, midnight, GMT
  #
  # FIXME: Change end time to be current date rounded down to 5 minute
  # interval, backing up two buckets for safety
  #end_epoch = 1428192000
  # For now use April 2nd, 02:00:00 GMT.  With 12 buckets of ids per hour, this gives us 25 calls
  end_epoch = 1427940000+1


  # Test stamp
  #scrape_games_for_timerange(region, api_key, 1428195600)


  # Go over all valid timestamps
  for t in range(start_epoch, end_epoch, 300):
    # make directory for each timestamp to store results in
    dump_subdir = str(t)
    #dump_subdir = dump_directory + os.sep + str(t)
    print dump_subdir
    os.mkdir(dump_subdir)
    os.chdir(dump_subdir)
    scrape_games_for_timerange(region, api_key, t)
    os.chdir("..")

def scrape_games_for_timerange(region, api_key, t):
  print "Scraping data from region " + region + ", epoch " +  str(t)

  
  logger = our_utils.Logger("query.log")

  game_ids = lac.api_challenge_game_ids(region, api_key, t, logger)

  logger.writeLog(json.dumps(game_ids))
  
  logger.closeLog()

  for gid in game_ids:
    #print gid
    subdir_name = str(gid)
    os.mkdir(subdir_name)
    os.chdir(subdir_name)

    logger = our_utils.Logger("query.log")

    match_detail = lac.get_match(region, api_key, gid, logger)

    logger.writeLog(json.dumps(match_detail))

    logger.closeLog()

    f = open("output.pretty", "w")
    f.write(our_utils.json_pretty_print(match_detail))
    f.close()
    os.chdir("..")
