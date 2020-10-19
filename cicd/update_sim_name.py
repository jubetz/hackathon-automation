#!/usr/bin/env python

import json
import sys
import os
import requests
from air_sdk import AirApi
from datetime import datetime, timedelta

#pull in some environment vars
ENVIRONMENT = os.getenv('CI_COMMIT_REF_NAME')

# set SITE var from args. Bail if not passed in.
if len(sys.argv) > 2:
    SITE = sys.argv[1]
    PARENT_PIPELINE_ID = sys.argv[2]
else:
    print("Arg error. Abort")
    sys.exit(1)

if "staging" in ENVIRONMENT:
    air = AirApi(api_url='https://staging.air.cumulusnetworks.com/api/', api_version='v1')
else:
    air = AirApi()

#air.authorize(username='<username>', password='<password>')

# Build the HTTP HEADERS with an auth token.
# can go away when sdk supports topology
HEADERS = {}
HEADERS["Authorization"] = "Bearer " + air.get_token(username=os.getenv('AIR_USERNAME'), password=os.getenv('AIR_PASSWORD'))

# Read in simlation data from sim clone/dup
duplicate_response = {}
with open('simulation_duplicate_response.json') as json_file:
    duplicate_response = json.load(json_file)

###### Update simulation with name for NetQ accont
simulation_url = duplicate_response["simulation"]["url"]

# calculate sleep/expires timers for CI run
now_time = datetime.now()
expires_at = now_time + timedelta(hours=24)
sleep_at = now_time + timedelta(hours=8)

# build the json body for the PUT to update the duplicated sim
simulation_put_data = {}
simulation_put_data["topology"] = duplicate_response["simulation"]["topology"]
simulation_put_data["name"] = SITE + ":" + PARENT_PIPELINE_ID
simulation_put_data["title"] = "CI Test Simulation"
simulation_put_data["expires_at"] = expires_at.isoformat()
simulation_put_data["sleep_at"] = sleep_at.isoformat()

# PUT to update the duplicated sim
try:
    simulation_put_response = requests.put(url=simulation_url, headers=HEADERS, json=simulation_put_data)
    simulation_put_response.raise_for_status()
    simulation_put_response = simulation_put_response.json()
except requests.exceptions.HTTPError as err:
    print("HTTP Error submitting the clone instructions!")
    print(err)
    sys.exit(1)

print("Simulation PUT/update response:")
print(json.dumps(simulation_put_response, indent=4))
print("Writing to file...")

with open('simulation_put_response.json', 'w') as outfile:
    json.dump(simulation_put_response, outfile)
