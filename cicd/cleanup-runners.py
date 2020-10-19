#!/usr/bin/env python

import gitlab
import os

TOKEN = os.getenv('API_KEY') # has write priv to actually delete runners: gitlab project var
#URL = "https://gitlab.com"
URL = os.getenv('CI_SERVER_URL')
PROJECT_ID = os.getenv('CI_PROJECT_ID')
CI_JOB_TOKEN = os.getenv('CI_JOB_TOKEN') # it's read-only

#gl = gitlab.Gitlab(URL, job_token=CI_JOB_TOKEN)
gl = gitlab.Gitlab(URL, private_token=TOKEN)

project = gl.projects.get(PROJECT_ID)

for p_runner in project.runners.list(all=True):
    try:
        if p_runner.attributes['status'] == "not_connected":
            print("Removing not connected/inactive runner:")
            print(p_runner)
            runner = gl.runners.get(p_runner.id)
            print(runner)
            runner.delete()
    # e.g. when runner is associated with multiple projects
    except Exception as ex:
        print(ex)
