import requests, base64, json, sys, argparse, os
from time import sleep
from argparse import RawTextHelpFormatter

cmd_session = requests.Session()

# Loads the environment variable as JSON structure
# We will use this later
Env_JSON = json.dumps(dict(**os.environ), sort_keys=True, indent=4)
EnvData = json.loads(Env_JSON)

header = {
    "Content-Type": "application/json"
}

if "GENEOS_PATH" in EnvData:
    GENEOS_PATH = EnvData["GENEOS_PATH"]

# payload for gateway to auto respond
payload = {
    # command to run
    "command" : "/SNOOZE:severityTo",
    "target" : GENEOS_PATH,
    "args": {
        "1": "Some Snooze Comment",
        "2": 3,
        "4": 1
    }
}

# Run post to PagerDuty Server
Gateway_Response = cmd_session.post('http://localhost:7039/rest/runCommand',
                        data=json.dumps(payload),
                        headers=header)
