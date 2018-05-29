#!/usr/bin/python
import requests, base64, json, sys, argparse, os
from argparse import RawTextHelpFormatter


SUBDOMAIN = "manny" # Enter your subdomain here
API_ACCESS_KEY = "QiaeVM4257psyzkVSs5Q" # Enter your subdomain's API access key here

# apiKey = "QiaeVM4257psyzkVSs5Q"
pagerduty_session = requests.Session()

def trigger_incident_without_key_name():
    """Triggers an incident with a previously generated incident key."""

    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={0}'.format(API_ACCESS_KEY),
        'Content-type': 'application/json',
    }

    payload = json.dumps({
        "service_key": "3e2966c4fe574b978ca0db7414d5e504", # Enter service key here
        "incident_key": "srv01/HTTP",
        "event_type": "trigger",
        "description": "FAILURE for production/HTTP on machine srv01.acme.com",
        "client": "Sample Monitoring Service",
        "client_url": "https://monitoring.service.com",
        "details": {
            "ping time": "1500ms",
            "load avg": 0.75
        }
    })

    PagerResponse = pagerduty_session.post('https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                      headers=headers,
                      data=payload,
    )

    print PagerResponse.status_code
    print PagerResponse.text

if __name__ == '__main__':
    # trigger_incident()
