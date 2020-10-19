#!/usr/bin/env python

import json
import sys
import os
import requests
import time
from air_sdk import AirApi

#pull in some environment vars
ENVIRONMENT = os.getenv('CI_COMMIT_REF_NAME')

if "staging" in ENVIRONMENT:
    air = AirApi(api_url='https://staging.air.cumulusnetworks.com/api/', api_version='v1')
else:
    air = AirApi()

#air.authorize(username='<username>', password='<password>')

# Build the HTTP HEADERS with an auth token.
HEADERS = {}
HEADERS["Authorization"] = "Bearer " + air.get_token(username=os.getenv('AIR_USERNAME'), password=os.getenv('AIR_PASSWORD'))


########## Delete the sim we cloned for test
# pull back in simulation PUT response from earlier job for details
simulation_response = {}
with open('simulation_put_response.json') as json_file:
    simulation_response = json.load(json_file)

print("Test sim response from duplication pulled back in:")
print(json.dumps(simulation_response, indent=4))

# generate the simulation control URL
simulation_control_url = simulation_response["url"] + "control/"

simulation_control_post_data = {}
simulation_control_post_data["action"] = "store"

#print("About to POST:")
#print(json.dumps(simulation_control_post_data, indent=4))

# POST to duplicate
#try:
#    simulation_control_response = requests.post(url=simulation_control_url, headers=HEADERS, json=simulation_control_post_data)
#    simulation_control_response.raise_for_status()
#    simulation_control_response = simulation_control_response.json()
#except requests.exceptions.HTTPError as err:
#    print("HTTP Error submitting the clone instructions!")
#    print(err)
#    sys.exit(1)

#print("Simulation control post response(destroy):")
#print(json.dumps(simulation_control_response, indent=4))
#print("Writing to file...")

#with open('simulation_destroy_response.json', 'w') as outfile:
#    json.dump(simulation_control_response, outfile)

print("")
print("")
print("Simulation Passed:")
print("")
print("Simulation Owner: " + simulation_response["name"])
print("Simulation Title: " + simulation_response["title"])
print("Simulation URL: " + simulation_response["url"])
print("Simulation ID: " + simulation_response["id"])
print("NetQ Username: " + simulation_response["netq_username"])
print("NetQ Password: " + simulation_response["netq_password"])
print("NetQ URL: https://air.netq.cumulusnetworks.com")
print("")
print("")

