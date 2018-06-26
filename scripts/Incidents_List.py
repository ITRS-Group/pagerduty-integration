#!/usr/bin/python
import requests, base64, json, sys, argparse, os
from argparse import RawTextHelpFormatter

# apiKey = "QiaeVM4257psyzkVSs5Q"
authorization_token = 'QiaeVM4257psyzkVSs5Q'
pagerduty_session = requests.Session()
pagerduty_session.headers.update({
  'Authorization': 'Token token=' + authorization_token,
  'Accept': 'application/vnd.pagerduty+json;version=2'
})

# Prep response for necessary results
User_List = pagerduty_session.get('https://api.pagerduty.com/incidents?statuses%5B%5D=acknowledged&statuses%5B%5D=triggered&time_zone=UTC&include%5B%5D=services')

# response.encoding = 'utf-8'
if User_List.status_code != 200:
    raise ValueError(
        'Request to PagerDuty a server returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

Incidents = User_List.json()
print(json.dumps(Incidents, indent=2))

for Incident in Incidents["incidents"]:
    #Print json response info to the screen
    print(json.dumps(Incident["incident_key"], indent=2))
