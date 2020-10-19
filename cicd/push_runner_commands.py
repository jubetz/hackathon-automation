#!/usr/bin/env python
"""Creates a test drive topology and simulation from the larger cldemo2 reference topology"""

import json
import sys
import os
import requests
from air_sdk import AirApi

#pull in some environment vars
ENVIRONMENT = os.getenv('CI_COMMIT_REF_NAME')
RUNNER_REG_TOKEN = os.getenv('RUNNER_REG_TOKEN') 

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

################
# pull in the artifact from the job where we performed PUT /simulation/id to update the name
simulation_put_response = {}
with open('simulation_put_response.json') as json_file:
    simulation_put_response = json.load(json_file)

## Pull out simulation_node list
node_list = simulation_put_response["nodes"]

print("NODE LIST:")
print(node_list)

for simulation_node_url in node_list:
    #get the simulation_node object and check the name for oob-mgmt-server and netq-ts
    #when true, set the gitlab-runner register command

    #print ("about to GET:")
    #print (simulation_node_url)
 
    try:
        simulation_node_response = requests.get(url=simulation_node_url, headers=HEADERS)
        simulation_node_response.raise_for_status()
        simulation_node_response = simulation_node_response.json()
    except requests.exceptions.HTTPError as err:
        print("Error fetching info for simulation_node")
        print(err)
        sys.exit(1)
    
    #print("GET Simulation_node response:")
    #print(json.dumps(simulation_node_response, indent=4))

    simulation_node_instruction_url = simulation_node_url + "instructions/"

    simulation_node_instruction_post_data = {}
    simulation_node_instruction_post_data["executor"] = "file"

    # check the name
    if simulation_node_response["name"] == "oob-mgmt-server":

        data = {}
        data["/home/cumulus/runner-script.sh"] = "passwd -x 99999 gitlab-runner\necho 'gitlab-runner:CumulusLinux!' | chpasswd\ngitlab-runner register --non-interactive --url https://gitlab.com --registration-token " + RUNNER_REG_TOKEN + \
            " --description oob-mgmt-server:" + SITE + ":" + PARENT_PIPELINE_ID + " --tag-list " + SITE + ":" + PARENT_PIPELINE_ID + ":oob-mgmt --executor shell"
        data["post_cmd"] = ["sh /home/cumulus/runner-script.sh"]

        simulation_node_instruction_post_data["data"] = json.dumps(data)

        print("About to POST:")
        print(json.dumps(simulation_node_instruction_post_data, indent=4))
        try:
            oob_mgmt_instruction_response = requests.post(url=simulation_node_instruction_url, headers=HEADERS, json=simulation_node_instruction_post_data)
            oob_mgmt_instruction_response.raise_for_status()
            oob_mgmt_instruction_response = oob_mgmt_instruction_response.json()
        except requests.exceptions.HTTPError as err:
            print("HTTP Error submitting the clone instructions!")
            print(err)
            sys.exit(1)
 
        print("oob_mgmt Instruction post response:")
        print(json.dumps(oob_mgmt_instruction_response, indent=4))
        print("Writing to file...")
        # write to file
        with open('oob_mgmt_instruction_response.json', 'w') as outfile:
            json.dump(oob_mgmt_instruction_response, outfile)
        
    elif simulation_node_response["name"] == "netq-ts":

        data = {}
        data["/home/cumulus/runner-script.sh"] = "passwd -x 99999 gitlab-runner\necho 'gitlab-runner:CumulusLinux!' | chpasswd\ngitlab-runner register --non-interactive --url https://gitlab.com --registration-token " + RUNNER_REG_TOKEN + \
            " --description netq-ts:" + SITE + ":" + PARENT_PIPELINE_ID + " --tag-list " + SITE + ":" + PARENT_PIPELINE_ID + ":netq-ts --executor shell"
        data["post_cmd"] = ["sh /home/cumulus/runner-script.sh"]

        simulation_node_instruction_post_data["data"] = json.dumps(data)

        print("About to POST:")
        print(json.dumps(simulation_node_instruction_post_data, indent=4))
        try:
            netq_ts_instruction_response = requests.post(url=simulation_node_instruction_url, headers=HEADERS, json=simulation_node_instruction_post_data)
            netq_ts_instruction_response.raise_for_status()
            netq_ts_instruction_response = netq_ts_instruction_response.json()
        except requests.exceptions.HTTPError as err:
            print("HTTP Error submitting the clone instructions!")
            print(err)
            sys.exit(1)

        print("NetQ-TS Instruction post response:")
        print(json.dumps(netq_ts_instruction_response, indent=4))
        print("Writing to file...")
        # write to file
        with open('netq_ts_instruction_response.json', 'w') as outfile:
            json.dump(netq_ts_instruction_response, outfile)

