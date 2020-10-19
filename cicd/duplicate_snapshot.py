#!/usr/bin/env python

import os
import requests
import json
import sys
import re
from air_sdk import AirApi

# this is the branch name
ENVIRONMENT = os.getenv('CI_COMMIT_REF_NAME')

# If the branch name has the word staging in it, then run against AIR staging env.
# else run against prod
if "staging" in ENVIRONMENT:
    TEMPLATE_SIMULATION_ID = "6b3d3c66-8373-47ff-ab32-56942caee0bd" # Live rev topology ID in STAGING
    air = AirApi(api_url='https://staging.air.cumulusnetworks.com/api/', api_version='v1')
    BASE_URL = "https://staging.air.cumulusnetworks.com/api/v1/" # staging
    BASE_SIMULATION = BASE_URL + "simulation/" + TEMPLATE_SIMULATION_ID + "/"
else:
    TEMPLATE_SIMULATION_ID = "79b77cda-ba81-4f69-b255-32da8b2255c4" # Live ref topology ID in PROD
    air = AirApi()
    BASE_URL = "https://air.cumulusnetworks.com/api/v1/" # prod
    BASE_SIMULATION = BASE_URL + "simulation/" + TEMPLATE_SIMULATION_ID + "/"

##########
ORG_MGMT_URL = BASE_URL + "organization/"
SIMULATION_MGMT_URL = BASE_URL + "simulation/"

air.authorize(username=os.getenv('AIR_USERNAME'), password=os.getenv('AIR_PASSWORD'))
# Build the HTTP HEADERS with an auth token.
# can go away when sdk supports topology
HEADERS = {}
HEADERS["Authorization"] = "Bearer " + air.get_token(username=os.getenv('AIR_USERNAME'), password=os.getenv('AIR_PASSWORD'))

##############
### GET the simulation by ID first, record a copy.
try:
    template_simulation_response = requests.get(url=BASE_SIMULATION, headers=HEADERS)
    template_simulation_response.raise_for_status()
    template_simulation_response = template_simulation_response.json()
except requests.exceptions.HTTPError as err:
    print("Error in trying to fetch cldemo2 topology AIR")
    print(err)
    sys.exit(1)

print ("Response from AIR: " + json.dumps(template_simulation_response,indent=4))

######### Duplicate the template simulation
# pull back in simulation response from artifact

# generate the simulation control URL
simulation_control_url = template_simulation_response["url"] + "control/"

simulation_control_post_data = {}
simulation_control_post_data["action"] = "duplicate"

print("About to POST:")
print(json.dumps(simulation_control_post_data, indent=4))

# POST to start the simulation
try:
    simulation_duplicate_response = requests.post(url=simulation_control_url, headers=HEADERS, json=simulation_control_post_data)
    simulation_duplicate_response.raise_for_status()
    simulation_duplicate_response = simulation_duplicate_response.json()
except requests.exceptions.HTTPError as err:
    print("HTTP Error submitting the clone instructions!")
    print(err)
    sys.exit(1)

print("Simulation control post response:")
print(json.dumps(simulation_duplicate_response, indent=4))

print("Writing to file...")

with open('simulation_duplicate_response.json', 'w') as outfile:
    json.dump(simulation_duplicate_response, outfile)
