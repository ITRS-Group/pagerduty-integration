import requests, base64, json, sys, argparse, os
from time import sleep
from argparse import RawTextHelpFormatter

cmd_session = requests.Session()

header = {
    "Content-Type": "application/json"
}

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
Gateway_Response = cmd_session.post('https://events.pagerduty.com/v2/enqueue',
                        data=json.dumps(payload),
                        headers=header)
