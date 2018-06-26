#!/usr/bin/python
import requests, base64, json, sys, argparse, os
from argparse import RawTextHelpFormatter

# Loads the environment variable as JSON structure
# We will use this later
Env_JSON = json.dumps(dict(**os.environ), sort_keys=True, indent=4)
EnvData = json.loads(Env_JSON)

# Pre-Reqs
SUBDOMAIN = "manny" # Enter your subdomain here
API_ACCESS_KEY = "QiaeVM4257psyzkVSs5Q" # Enter your subdomain's API access key here
SERVICE_KEY = "3e2966c4fe574b978ca0db7414d5e504" # Variablize this value

#Incident Key (x,y of our geneos integration)
INCIDENT_KEY = EnvData["_GATEWAY"] + "\\" + EnvData["_PROBE"] + "\\" + EnvData["_SAMPLER"] + "\\" + EnvData["_MANAGED_ENTITY"] + "\\" + EnvData["_DATAVIEW"] + "\\" + EnvData["_COLUMN"] + "\\" + EnvData["_ROWNAME"]

# For Testing the script, in leiu of any proxy configuration to test against
# export _GATEWAY="SomeGateway"
# export _PROBE="SomeProbe"
# export _SAMPLER="SomeSampler"
# export _MANAGED_ENTITY="SomeEntity"
# export _DATAVIEW="SomeDataview"
# export _ROWNAME="SomeRowName"

# apiKey = "QiaeVM4257psyzkVSs5Q"
pagerduty_session = requests.Session()

def event_trigger_incident():
    """Triggers an incident with a previously generated incident key via Events API."""

    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={0}'.format(API_ACCESS_KEY),
        'Content-type': 'application/json',
    }

    payload = json.dumps({
        "service_key": "3e2966c4fe574b978ca0db7414d5e504", # Enter service key here
        "incident_key": INCIDENT_KEY,
        "event_type": "trigger",
        "description": "CRITICAL ITS ON FIRE for production/HTTP on machine srv01.acme.com",
        "client": "Sample Monitoring Service",
        "client_url": "https://monitoring.service.com",
        "details": {
            "_SEVERITY" : EnvData["_SEVERITY"],
            "_PREVIOUS_SEVERITY" : EnvData["_PREVIOUS_SEV"]
        }
    })

    PagerResponse = pagerduty_session.post('https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                      headers=headers,
                      data=payload,
    )

    # response.encoding = 'utf-8'
    if PagerResponse.status_code != 200:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
            )

    # Load up the Checks found
    # Check_Found = PagerResponse.json()

    # Print json response info to the screen
    print(json.dumps(PagerResponse.json(), indent=2))

def event_ack_incident():
    """Acknowledges a triggered incident using the customer's API access key and incident key via Events API."""

    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={0}'.format(API_ACCESS_KEY),
        'Content-type': 'application/json'
    }

    payload = json.dumps({
        "service_key": "3e2966c4fe574b978ca0db7414d5e504", # Enter service key here
        "incident_key": INCIDENT_KEY, # Enter incident key here
        "event_type": "acknowledge",
        "description": "Andrew now working on the problem.", # Enter your own description
        "details": {
            "_SEVERITY" : EnvData["_SEVERITY"],
            "_PREVIOUS_SEVERITY" : EnvData["_PREVIOUS_SEV"]
        }
    })

    PagerResponse = pagerduty_session.post('https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                      headers=headers,
                      data=payload,
    )

    # response.encoding = 'utf-8'
    if PagerResponse.status_code != 200:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
            )

    # Load up the Checks found
    # Check_Found = PagerResponse.json()

    # Print json response info to the screen
    print(json.dumps(PagerResponse.json(), indent=2))

def event_resolve_incident():
    """Resolves a PagerDuty incident using customer's API access key and incident key via Events API."""

    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={0}'.format(API_ACCESS_KEY),
        'Content-type': 'application/json',
    }

    payload = json.dumps({
        "service_key": "3e2966c4fe574b978ca0db7414d5e504", # Enter service key here
        "incident_key": INCIDENT_KEY, # Enter incident key here
        "event_type": "resolve",
        "description": "Some dude fixed the problem.", # Enter personalized description
        "details": {
            "_SEVERITY" : EnvData["_SEVERITY"],
            "_PREVIOUS_SEVERITY" : EnvData["_PREVIOUS_SEV"]
        }
    })

    PagerResponse = pagerduty_session.post('https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                      headers=headers,
                      data=payload,
    )

    # response.encoding = 'utf-8'
    if PagerResponse.status_code != 200:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
            )

    # Load up the Checks found
    # Check_Found = PagerResponse.json()

    # Print json response info to the screen
    print(json.dumps(PagerResponse.json(), indent=2))

def agent_trigger_incident():
    """Triggers an incident with a previously generated incident key via PDAgent."""

    # Print json response info to the screen
    # print(json.dumps(PagerResponse.json(), indent=2))

def agent_ack_incident():
    """Acknowledges a triggered incident using the customer's API access key and incident key via PDAgent."""

    # Print json response info to the screen
    # print(json.dumps(PagerResponse.json(), indent=2))

def agent_resolve_incident():
    """Resolves a PagerDuty incident using customer's API access key and incident key via PDAgent."""

    # Print json response info to the screen
    # print(json.dumps(PagerResponse.json(), indent=2))

if __name__ == '__main__':
    if (EnvData["_SEVERITY"] == "CRITICAL"):
        # Trigger or Update an open incident
        event_trigger_incident()
    if (EnvData["_SEVERITY"] == "WARNING") :
        # Acknowledges an incident
        event_ack_incident()
    if (EnvData["_SEVERITY"] == "OK") or (EnvData["_SEVERITY"] == "UNDEFINED"):
        # Trigger or Update an open incident
        event_resolve_incident()
