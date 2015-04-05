#!/usr/bin/env python

import json

def json_pretty_print(j):
  return json.dumps(j, sort_keys = True, indent = 2, separators = (",", ":"))
