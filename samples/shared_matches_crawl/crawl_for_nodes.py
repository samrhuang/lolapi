#!/usr/bin/env python

import urllib2
import json
import sys
import Queue
import time
import datetime
#import socket

def bootstrap_challenger():

  # Establish region and api root for everything but static calls
  region = "na"
  lol_api_root = "https://na.api.pvp.net/api/lol/" + region

  #print socket.getdefaulttimeout()
  #socket.setdefaulttimeout(30)

  # Read in dev api key
  api_key_file = "api_key"

  f = open(api_key_file, 'r')
  api_key = f.read().strip()
  f.close()

  auth = "api_key=" + api_key

  # Grab the list of challengers
  url_req = lol_api_root + "/v2.5/league/challenger?type=RANKED_SOLO_5x5&" + auth
  f = make_api_call(url_req)
  league_dto = json.loads(f.read())
  f.close()

  # Create map of challengers with IDs as keys and summoner names as values
  challenger_info = dict()
  map(lambda x: challenger_info.update({x.get("playerOrTeamId"): standardize_summoner_name(x.get("playerOrTeamName"))}), league_dto.get("entries"))


  # Create map of all known summoners, starting with challenger list
  summoner_id2name = dict()
  summoner_id2name.update(challenger_info)
  summoner_name2id = dict([reversed(i) for i in summoner_id2name.items()])
  #print json_pretty_print(summoner_id2name)
  #print json_pretty_print(summoner_name2id)

  # Create queue of novel summoners whose summoner names are known but ids are not.  They will be queried for their ids in batches.
  names_to_query = Queue.Queue()
  names_to_query_set = set()

  # Create queue of all summoners ids to inspect
  to_visit = Queue.Queue()
  for id in challenger_info.keys():
    to_visit.put(id)

  # Take a summoner id off the top and grap recent games.  Find all summoners who played in the match with 
#if not to_visit.empty():
  while not to_visit.empty():
    print "Number of summoners found: " + str(len(summoner_id2name.items()))
    summoner_id = to_visit.get()
    print "Looking up match history for summoner " + summoner_id2name[summoner_id] + " (" + summoner_id + ")"

    url_req = lol_api_root + "/v2.2/matchhistory/" + summoner_id + "?" + auth
    f = make_api_call(url_req)
    summoner_matches = json.loads(f.read())
    f.close()

    # Iterate over all matches grabbed by match history.
    # TODO: Add a set to track all matches queried so far; it will prevent
    # duplicate queries made about the same match over different users.
    for m in summoner_matches.get("matches"):

      url_req = lol_api_root + "/v2.2/match/" + str(m.get("matchId")) + "?" + auth
      f = make_api_call(url_req)
      match_summary = json.loads(f.read())
      f.close()

      fmt = "%Y-%m-%d %H:%M:%S"
      print "Processing match " + str(match_summary.get("matchId")) + " which started at " + datetime.datetime.fromtimestamp(match_summary.get("matchCreation")/1000).strftime(fmt) + " and lasted for " + str(datetime.timedelta(seconds=match_summary.get("matchDuration")))
      partID_entries = match_summary.get("participantIdentities")
      for p in partID_entries:
        summoner_name = standardize_summoner_name(p.get("player").get("summonerName"))

        # If the name isn't already registered or already in line to be registerd, add it to the queue for registry
        if summoner_name not in summoner_name2id and summoner_name not in names_to_query_set:
          names_to_query.put(summoner_name)
          names_to_query_set.add(summoner_name)

    #print len(names_to_query_set)

    #print len(names_to_query_set), len(summoner_id2name)
    # Form new summoner id query whenever we have at least 40 summoners in line to be queried.
    while len(names_to_query_set) > 40: # Magic number given by Riot
      query_set = []
      for i in range(40):
        next_name = names_to_query.get()
        names_to_query_set.remove(next_name)
        query_set.append(next_name)
      #print len(query_set)

      url_req = lol_api_root + "/v1.4/summoner/by-name/" + ",".join(query_set) + "?" + auth
      f = make_api_call(url_req)
      summoner_dtos = json.loads(f.read())
      f.close()


      #print len(summoner_dtos)
      #print json_pretty_print(summoner_dtos)
      for (sname, sdto) in summoner_dtos.items():
#print sname, sdto
        _sum_name = standardize_summoner_name(sdto.get("name"))
        _sum_id = sdto.get("id")
        summoner_id2name[_sum_id] = _sum_name
        summoner_name2id[_sum_name] = _sum_id
        to_visit.put(_sum_id)

    #print len(names_to_query_set), len(summoner_id2name)

      


# Performs actual request/call to lol api, returning a file descriptor from
# urllib allowing one to access result.  Handles HTTP Error code 429 (Rate
# limit exceeded), applying exponential backoff with repeated request.
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
    else:
      # Throw the rest back!
      raise e


def make_api_call_helper(url):
#req = urllib2.Request(url)
  try:
    req = urllib2.Request(url.encode())
    return urllib2.urlopen(req)
  except UnicodeEncodeError:
    print "Uh-oh... problems with: " + url
    raise

# Standardized names are all lowercase and have spaces removed
def standardize_summoner_name(name):
  standard = "".join(name.lower().split())
#print name + " --> " + standard
  return standard


def json_pretty_print(j):
  return json.dumps(j, sort_keys = True, indent = 2, separators = (",", ":"))

def main():
  bootstrap_challenger()


if __name__ == "__main__":
  main()
