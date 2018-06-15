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
User_List = pagerduty_session.get('https://api.pagerduty.com/incidents')

# response.encoding = 'utf-8'
if User_List.status_code != 200:
    raise ValueError(
        'Request to PagerDuty a server returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

#Print json response info to the screen
print(json.dumps(User_List.json(), indent=2))
