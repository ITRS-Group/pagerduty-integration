#!/usr/bin/python
import requests, base64, json, sys, argparse, os
import urllib3
from argparse import RawTextHelpFormatter

# For Supressing warnings
# urllib3.disable_warnings()

# Loads the environment variable as JSON structure
# We will use this later
Env_JSON = json.dumps(dict(**os.environ), sort_keys=True, indent=4)
EnvData = json.loads(Env_JSON)

# Pre-Reqs
SUBDOMAIN = "manny" # Enter your subdomain here
API_ACCESS_KEY = "QiaeVM4257psyzkVSs5Q" # Enter your subdomain's API access key here
SERVICE_KEY = "3e2966c4fe574b978ca0db7414d5e504" # Variablize this value
GENEOS_PAYLOAD = {} # Massive Payload of geneos information

# Incident Key (x,y of our geneos integration)
# WARNING :: PagerDuty has 255 Character Limit
INCIDENT_KEY = EnvData["_GATEWAY"] + "\\" + EnvData["_PROBE"] + "\\" + EnvData["_MANAGED_ENTITY"] + "\\" + EnvData["_SAMPLER"] + "\\" + EnvData["_DATAVIEW"] + "\\" + EnvData["_ROWNAME"] + "\\" + EnvData["_COLUMN"]

# For Testing the script, in leiu of any proxy configuration to test against
 # export _GATEWAY="SomeGateway"
 # export _PROBE="SomeProbe"
 # export _SAMPLER="SomeSampler"
 # export _MANAGED_ENTITY="SomeEntity"
 # export _DATAVIEW="SomeDataview"
 # export _ROWNAME="SomeRowName"
 # export _SEVERITY="CRITICAL"
 # export _PREVIOUS_SEV="2"

# apiKey = "QiaeVM4257psyzkVSs5Q"
pagerduty_session = requests.Session()

# Incident interactions
def event_trigger_incident():
    # Triggers a PagerDuty incident without a previously generated incident key
    # Uses Events V2 API - documentation: https://v2.developer.pagerduty.com/docs/send-an-event-events-api-v2

    header = {
        "Content-Type": "application/json"
    }

    payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "trigger",
        "dedup_key": INCIDENT_KEY,
        "integration_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Alert on " + EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"] + " " + EnvData["_ROWNAME"] + " : " + EnvData["_COLUMN"] + " at " + EnvData["_VALUE"],
            "severity": "critical",
            "source" : EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "custom_details" : {
                "Geneos Event Data" : {
                    "_SEVERITY" : EnvData["_SEVERITY"]
                },
                "Custom Message" : "Use custom detailed here Message"
            }
        }
    }

    # Re-Cconstruct Payload for Geneos Event Data
    for EnvKey in EnvData:
        if EnvKey.startswith("_"):
            payload["payload"]["custom_details"]["Geneos Event Data"][EnvKey] = EnvData[EnvKey]

    # Run post to PagerDuty Server
    PagerResponse = pagerduty_session.post('https://events.pagerduty.com/v2/enqueue',
                            data=json.dumps(payload),
                            headers=header)

    # response.encoding = 'utf-8'
    if PagerResponse.status_code != 202:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (PagerResponse.status_code, PagerResponse.text)
            )

    # If all is good
    if PagerResponse.json()["status"] == "success":
        print ('Incident Created')
    else:
        print PagerResponse.text # print error message if not successful

    # Print json response info to the screen
    print(json.dumps(PagerResponse.json(), indent=2))

def event_ack_incident():
    """Acknowledges a triggered incident using the customer's API access key and incident key via Events API."""

    header = {
        "Content-Type": "application/json"
    }

    payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "acknowledge",
        "dedup_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Acknowledged on " + EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "severity": "warning",
            "source" : EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "custom_details" : {
                "Geneos Event Data" : {
                    "_SEVERITY" : EnvData["_SEVERITY"]
                },
                "Custom Message" : "Use custom detailed here Message"
            }
        }
    }

    # Re-Cconstruct Payload for Geneos Event Data
    for EnvKey in EnvData:
            if EnvKey.startswith("_"):
                payload["payload"]["custom_details"]["Geneos Event Data"][EnvKey] = EnvData[EnvKey]

    # Post to PagerDuty Server
    PagerResponse = pagerduty_session.post('https://events.pagerduty.com/v2/enqueue',
                            data=json.dumps(payload),
                            headers=header)
    # If all is good
    if PagerResponse.json()["status"] == "success":
        print ('Incident Acknowledged ')
    else:
        print PagerResponse.text # print error message if not successful

    # response.encoding = 'utf-8'
    if PagerResponse.status_code != 202:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (PagerResponse.status_code, PagerResponse.text)
            )

    # Load up the Checks found
    # Check_Found = PagerResponse.json()

    # Print json response info to the screen
    print(json.dumps(PagerResponse.json(), indent=2))

def event_resolve_incident():
    """Resolves a PagerDuty incident using customer's API access key and incident key via Events API."""

    header = {
        "Content-Type": "application/json"
    }

    # JSON payload
    payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "resolve",
        "dedup_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Resolved on " + EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "severity": "info",
            "source" : EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "custom_details" : {
                "Geneos Event Data" : {
                    "_SEVERITY" : EnvData["_SEVERITY"]
                },
                "Custom Message" : "Use custom detailed here Message"
            }
        }
    }

    PagerResponse = pagerduty_session.post('https://events.pagerduty.com/v2/enqueue',
                            data=json.dumps(payload),
                            headers=header)

    if PagerResponse.json()["status"] == "success":
        print ('Incident Resolved ')
    else:
        print PagerResponse.text # print error message if not successful

    # response.encoding = 'utf-8'
    if PagerResponse.status_code != 202:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (PagerResponse.status_code, PagerResponse.text)
            )

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
