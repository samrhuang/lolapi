#!/usr/bin/env python

import urllib2
import json
import sys



def main():
  region = "na"
  lol_api_root = "https://na.api.pvp.net/api/lol/" + region


  api_key_file = "api_key"

  f = open(api_key_file, 'r')
  api_key = f.read().strip()
  f.close()

  auth = "?api_key=" + api_key

  if len(sys.argv) > 1:
    summoner_name = sys.argv[1]
  else:
    print "Enter the name of a summoner you wish to look up: "
    summoner_name = sys.stdin.readline().strip()

  req = urllib2.Request(lol_api_root + "/v1.4/summoner/by-name/" + summoner_name + auth)
  f = urllib2.urlopen(req)
  summoner_obj = json.loads(f.read())
  f.close()
  summoner_id = summoner_obj.get(summoner_name).get("id")

  print "Id is", summoner_id


  req = urllib2.Request(lol_api_root + "/v2.5/league/by-summoner/" + str(summoner_id) + "/entry" + auth)
  f = urllib2.urlopen(req)
  league_entries = json.loads(f.read())
  f.close()

  summoner_entries = league_entries.get(str(summoner_id))

  #print league_entries.keys()

  for s_e in summoner_entries:
    print "Good job " + summoner_name + ", you've made it to " + s_e.get("tier") + " tier, division", s_e.get("entries")[0].get("division") + ", titled \"" + s_e.get("name") +  "\" for " + s_e.get("queue") + "!"


def json_pretty_print(j):
  return json.dumps(j, sort_keys = True, indent = 2, separators = (",", ":"))

if __name__ == "__main__":
  main()
