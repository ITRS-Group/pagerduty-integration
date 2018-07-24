import requests, base64, json, sys, argparse, os, time
import urllib3
from datetime import datetime
from argparse import RawTextHelpFormatter

# For Supressing warnings
# urllib3.disable_warnings()

#Uber ASCII Art
Uber_Small_ASCII = ("" + \
"                .,coxOKXNWMWl                               \n" + \
"            .;okKWMMMMMMMMMWl               ..              \n" + \
"         .:xKWMMMMMMMMMMMMMWd....          'k0d;.           \n" + \
"       'o0WMMMMMMMMMMMMMMMMMNXKKKOkdl:'.  ;0WMMW0l.         \n" + \
"     .dXMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNKxxKMMMMMMWXo.       \n" + \
"   .lKMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKl.     \n" + \
"  'kWMMMMMMMMMMMMMMMMMWX0OxxxxxkO0XWMMMMMMMMMMMMMMMMMWk'    \n" + \
" .dNMMMMMMMMMMMMMMW0dc,..        ..,cxKWMMMMMMMMMMMMMMM0;   \n" + \
"  .'lkXWMMMMMMMMXx;.                  .;xXMMMMMMMMMMMMMMK:  \n" + \
"      lNMMMMMMXd'                        'dNMMMMMMMMMMMMM0, \n" + \
"     ,0MMMMMM0;                            :0WMMMMMMMMMMMWk.\n" + \
"    .kWMMMMMO'                              ,OMMMMMMMMMMMMNc\n" + \
"    cNMMMMMK;           'lxO0OOxl'           ;KMMMMMMMMMMMMO\n" + \
"   .xMMMMMWo          .dNMMMMMMMMXd.         .dWMMMMMMMMMMMX\n" + \
"   .OMMMMMX:         .dWMMMMMMMMMMWo          :NMMMMMMMMMMMN\n" + \
"'odkNMMMMMK;         .kMMMMMMMMMMMMk.         ;XMMMMMMMMWk:;\n" + \
":NMMMMMMMMN:          cXMMMMMMMMMMX:          cNMMMMMMMMX:  \n" + \
",KMMMMMMMMWx.          ;kNWMMMMWNk;          .xMMMMMMMMM0'  \n" + \
".xWMMMMMMMMX:            ':lllc:'            cXMMMMMMMMWd.  \n" + \
" ;KMMMMMMMMMK:                              :KMMMMMMMMMK,   \n" + \
"  lNMMMMMMMMMXl.                          .oXMMMMMMMMMNl    \n" + \
"  .oNMMMMMMMMMWO:.                      .:OWMMMMMMMMMNo.    \n" + \
"   .lXMMMMMMMMMMW0l'.                .,o0WMMMMMMMMMMXl.     \n" + \
"     :0WMMMMMMMMMMMN0dc;'........';ld0NMMMMMMMMMMMW0;       \n" + \
"      .oXMMMMMMMMMMMMMMWNXK000KKXNWMMMMMMMMMMMMMMXo.        \n" + \
"        'dXWMMMWWMMMMMMMMMMMMMMMMMMMMMMMWWMMMMWXd'          \n" + \
"          .lONNd;cdOXWWMMMMMMMMMMMMWWXOdc:kNNOl.            \n" + \
"            .cc.   .,cx0XNWWMWWWNKOxc,.   .oc.              \n\n" + \
"         - Geneos Integrations for PagerDuty -     \n" )

# Modify Environment variables
Usage_Msg = ( Uber_Small_ASCII + \
"\n\tExample for resolving a PagerDuty incident:\n\n" + \
"\t\t" + sys.argv[0] + " -r \"MyGateway\\MyProbe\\MySampler\\MyDataview\\MyIncident\"\n" + \
"\n\tExample for acknowledging a PagerDuty incident:\n\n" + \
"\t\t" + sys.argv[0] + " -a \"MyGateway\\MyProbe\\MySampler\\MyDataview\\MyIncident\"\n")

# Arg Parser https://stackoverflow.com/questions/15753701/argparse-option-for-passing-a-list-as-option https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser( description= Usage_Msg , formatter_class=RawTextHelpFormatter)

# Typical operations for PagerDuty
parser.add_argument( "-r", "--resolve", help = "resolves targeted Incident",  type=str)
parser.add_argument( "-a", "--acknowledge", help = "acknowledges targeted Incident",  type=str)
parser.add_argument( "-t", "--trigger", help = "triggers and creates an Incident in PagerDuty, if no Incident Key is provided then one is generated",  type=str)

# global args
args = parser.parse_args()

# Loads the environment variable as JSON structure
# We will use this later
Env_JSON = json.dumps(dict(**os.environ), sort_keys=True, indent=4)
EnvData = json.loads(Env_JSON)

# Pre-Reqs
API_ACCESS_KEY = "QiaeVM4257psyzkVSs5Q" # Enter your subdomain's API access key here
SERVICE_KEY = "3e2966c4fe574b978ca0db7414d5e504" # Variablize this value
GENEOS_PAYLOAD = {} # Massive Payload of geneos information

# Incident Key (x,y of our geneos integration)
# WARNING :: PagerDuty has 255 Character Limit
if not (args.acknowledge) and not (args.trigger) and not (args.resolve):
    INCIDENT_KEY = EnvData["_GATEWAY"] + "\\" + EnvData["_PROBE"] + "\\" + EnvData["_MANAGED_ENTITY"] + "\\" + EnvData["_SAMPLER"] + "\\" + EnvData["_DATAVIEW"] + "\\" + EnvData["_ROWNAME"] + "\\" + EnvData["_COLUMN"]
elif (args.acknowledge):
    INCIDENT_KEY = (args.acknowledge)
elif (args.trigger):
    INCIDENT_KEY = (args.trigger)
elif (args.resolve):
    INCIDENT_KEY = (args.resolve)
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

# time now
unix_time = time.time()
human_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Incident interactions
def event_trigger_incident():
    # Triggers a PagerDuty incident without a previously generated incident key
    # Uses Events V2 API - documentation: https://v2.developer.pagerduty.com/docs/send-an-event-events-api-v2

    header = {
        "Content-Type": "application/json"
    }

    if(args.trigger):
        payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "trigger",
        "dedup_key": INCIDENT_KEY,
        "integration_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Alerted from an Active Console",
            "severity": "critical",
            "source" : "Active Console",
            "custom_details" : {
                "Geneos Event Data" : {
                    "HUMAN_TIME" : human_time,
                    "UNIX_TIME" : unix_time
                },
                "Custom Message" : "Use custom detailed here Message"
            }
        }
        }
    else:
        payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "trigger",
        "dedup_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Alert on " + EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"] + " - Date: " + human_time + " - Row: " + EnvData["_ROWNAME"] + " : " + EnvData["_COLUMN"] + " at " + EnvData["_VALUE"],
            "severity": "critical",
            "source" : EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "custom_details" : {
                "Geneos Event Data" : {
                    "HUMAN_TIME" : human_time,
                    "UNIX_TIME" : unix_time,
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

    if (args.acknowledge):
        payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "acknowledge",
        "dedup_key": INCIDENT_KEY,
        "integration_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Acknowledged on Active Console",
            "severity": "warning",
            "source" : "Manualy Acknowledged",
            "custom_details" : {
                "Geneos Event Data" : {
                    "HUMAN_TIME" : human_time,
                    "UNIX_TIME" : unix_time
                },
                    "Custom Message" : "Use custom detailed here Message"
            }
            }
        }
    else:
        payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "acknowledge",
        "dedup_key": INCIDENT_KEY,
        "integration_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Acknowledged on " + EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "severity": "warning",
            "source" : EnvData["_PROBE"] + "/" + EnvData["_HOSTNAME"],
            "custom_details" : {
                "Geneos Event Data" : {
                    "HUMAN_TIME" : human_time,
                    "UNIX_TIME" : unix_time,
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

    if (args.resolve):
        # JSON payload
        payload = { # Payload is built with the least amount of fields required to trigger an incident
        "routing_key": SERVICE_KEY,
        "event_action": "resolve",
        "dedup_key": INCIDENT_KEY,
        "payload": {
            "summary" : "Resolved from Active Console",
            "severity": "info",
            "source" : "from Active Console",
            "custom_details" : {
                "Geneos Event Data" : {
                    "HUMAN_TIME" : human_time,
                    "UNIX_TIME" : unix_time
                },
                "Custom Message" : "Use custom detailed here Message"
            }
        }
        }
    else:
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
                    "HUMAN_TIME" : human_time,
                    "UNIX_TIME" : unix_time
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

if __name__ == '__main__':
    if (args.acknowledge):
        # user_ack_incident(args.acknowledge)
        event_ack_incident()
    elif (args.resolve):
        # user_resolve_incident(args.resolve)
        event_resolve_incident()
    elif (args.trigger):
        # user_trigger_incident(args.trigger)
        event_trigger_incident()
    elif "_SEVERITY" in EnvData:
        if (EnvData["_SEVERITY"] == "CRITICAL"):
            # Trigger or Update an open incident
            event_trigger_incident()
        if (EnvData["_SEVERITY"] == "WARNING") :
            # Acknowledges an incident
            event_ack_incident()
        if (EnvData["_SEVERITY"] == "OK") or (EnvData["_SEVERITY"] == "UNDEFINED"):
            # Trigger or Update an open incident
            event_resolve_incident()
