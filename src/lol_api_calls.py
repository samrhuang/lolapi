#!/usr/bin/env python

import urllib2
import json
import time

# Module for making all the different api calls to the LoL api.  Commonly
# region and api key are needed, in addition to whatever other parameters are
# required.
#
# Consult https://developer.riotgames.com/api/methods for full api reference.
#
# TODO: Add appropriate safety checking, etc to these calls.
#

# Base root location of the lol api.
lol_api_root = "https://na.api.pvp.net"


# Method to performs actual request/call to lol api, returning a file
# descriptor from urllib allowing one to access result.  Handles HTTP Error
# code 429 (Rate limit exceeded), applying exponential backoff with repeated
# request.
def make_api_call(url):
  print "++ Making call from: " + url
  try:
    return make_api_call_helper(url)
  except urllib2.HTTPError as e:

    # Rate limit exceeded
    if e.code == 429:
      print "OVER THE LIMIT, SUCKA!"
      # Wait and try again, using exponential backoff
      completed = False
      wait_time = 1
      while not completed:
        try:
          print "Waiting for " + str(wait_time) + " seconds."
          time.sleep(wait_time)
          return make_api_call_helper(url)
        except urllib2.HTTPError:
           wait_time *= 2
    elif e.code == 400:
      # Could handle differently
      raise e
    else:
      # Throw the rest back!
      raise e


def make_api_call_helper(url):
  try:
    req = urllib2.Request(url.encode())
    return urllib2.urlopen(req)
  except UnicodeEncodeError:
    print "Uh-oh... problems with: " + url
    raise

# Get a list of game IDs for a 5 minute time range, starting with the given date.  beginDate is in epoch time.
def api_challenge_game_ids(region, api_key, beginDate):

  call_string = lol_api_root + "/api/lol/" + region + "/v4.1/game/ids?beginDate=" + str(beginDate) + "&api_key=" + api_key

  f = make_api_call(call_string)
  output = f.read()
  return json.loads(output)
#print output
#print "Heya!"





# TODO: Convert the remaining paths to function calls for this module.

#/api/lol/{region}/v1.2/champion
#/api/lol/{region}/v1.2/champion/{id}
#/observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}
#/observer-mode/rest/featured
#/api/lol/{region}/v1.3/game/by-summoner/{summonerId}/recent
#/api/lol/{region}/v2.5/league/by-summoner/{summonerIds}
#/api/lol/{region}/v2.5/league/by-summoner/{summonerIds}/entry
#/api/lol/{region}/v2.5/league/by-team/{teamIds}
#/api/lol/{region}/v2.5/league/by-team/{teamIds}/entry
#/api/lol/{region}/v2.5/league/challenger
#/api/lol/static-data/{region}/v1.2/champion
#/api/lol/static-data/{region}/v1.2/champion/{id}
#/api/lol/static-data/{region}/v1.2/item
#/api/lol/static-data/{region}/v1.2/item/{id}
#/api/lol/static-data/{region}/v1.2/language-strings
#/api/lol/static-data/{region}/v1.2/languages
#/api/lol/static-data/{region}/v1.2/map
#/api/lol/static-data/{region}/v1.2/mastery
#/api/lol/static-data/{region}/v1.2/mastery/{id}
#/api/lol/static-data/{region}/v1.2/realm
#/api/lol/static-data/{region}/v1.2/rune
#/api/lol/static-data/{region}/v1.2/rune/{id}
#/api/lol/static-data/{region}/v1.2/summoner-spell
#/api/lol/static-data/{region}/v1.2/summoner-spell/{id}
#/api/lol/static-data/{region}/v1.2/versions
#/shards
#/shards/{region}

def get_match(region, api_key, matchId):
  #/api/lol/{region}/v2.2/match/{matchId}
  call_string = lol_api_root + "/api/lol/" + region + "/v2.2/match/" + str(matchId) + "?api_key=" + api_key
  f = make_api_call(call_string)
  return json.loads(f.read())

#/api/lol/{region}/v2.2/matchhistory/{summonerId}
#/api/lol/{region}/v1.3/stats/by-summoner/{summonerId}/ranked
#/api/lol/{region}/v1.3/stats/by-summoner/{summonerId}/summary
#/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}
#/api/lol/{region}/v1.4/summoner/{summonerIds}
#/api/lol/{region}/v1.4/summoner/{summonerIds}/masteries
#/api/lol/{region}/v1.4/summoner/{summonerIds}/name
#/api/lol/{region}/v1.4/summoner/{summonerIds}/runes
#/api/lol/{region}/v2.4/team/by-summoner/{summonerIds}
#/api/lol/{region}/v2.4/team/{teamIds}
