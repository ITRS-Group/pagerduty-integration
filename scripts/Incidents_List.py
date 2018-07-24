import requests, base64, json, sys, argparse, os
from time import sleep
from argparse import RawTextHelpFormatter

# apiKey = "QiaeVM4257psyzkVSs5Q"
authorization_token = 'QiaeVM4257psyzkVSs5Q'
pagerduty_session = requests.Session()
pagerduty_session.headers.update({
  'Authorization': 'Token token=' + authorization_token,
  'Accept': 'application/vnd.pagerduty+json;version=2'
})

# Limit for num of inicdents (This you can tweak)
Pagination_Limit = 10

# Assume Offset is None
Offset = 0

# Our_Incidents
DV_Incidents = {}

# list out all of the alerts for incident
def List_Alerts(Incident_ID):

    # URL for the incident in inquiry
    Incident_Alerts_Url = "https://api.pagerduty.com/incidents/" + str(Incident_ID) + "/alerts?sort_by=created_at%3Adesc"

    # print Inicident_Alerts_Url

    # Starting_URL = "https://api.pagerduty.com/incidents?statuses%5B%5D=triggered&statuses%5B%5D=acknowledged&time_zone=UTC&include%5B%5D=first_trigger_log_entries&include%5B%5D=assignees&include%5B%5D=acknowledgers&total=true&limit=" + str(Pagination_Limit)
    Alerts_list = pagerduty_session.get(Incident_Alerts_Url)

    # response.encoding = 'utf-8'
    if Alerts_list.status_code != 202 and Alerts_list.status_code != 200:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (Alerts_list.status_code, Alerts_list.text)
        )

    Alerts = Alerts_list.json()
    # print(json.dumps(Alerts, indent=2))
    DV_Incidents[Incident_ID]["alert_id"] = Alerts["alerts"][0]["id"]
    DV_Incidents[Incident_ID]["alert_summary"] = Alerts["alerts"][0]["summary"]
    # print Alerts["alerts"][0]["id"]

    # return Alerts_Details
    # Get_Alerts_Url = "https://api.pagerduty.com/incidents/" + str(Incident_ID) + "/alerts/" + Alerts["alerts"][0]["id"]
    #
    # # make the call
    # Alerts_Details_Call = pagerduty_session.get(Get_Alerts_Url)
    #
    # # response.encoding = 'utf-8'
    # if Alerts_Details_Call.status_code != 202 and Alerts_Details_Call.status_code != 200:
    #     raise ValueError(
    #         'Request to PagerDuty a server returned an error %s, the response is:\n%s'
    #         % (Alerts_Details_Call.status_code, Alerts_Details_Call.text)
    #     )
    #
    #
    # Alert_Details = Alerts_Details_Call.json()
    # print(json.dumps(Alert_Details, indent=2))


# function to call to add to your incident list
def Update_Incident_List(JSON_Payload):

    # list out your incidents
    for Incident in JSON_Payload["incidents"]:

        # Print json response info to the screen
        bGeneosIncidents = False

        # Geneos_Path = "Not Geneos Alert Generated Inicident"
        Geneos_Path = ""

        # print(json.dumps(Incident, indent=2))
        if "channel" in Incident["first_trigger_log_entry"]:
            if "details" in Incident["first_trigger_log_entry"]["channel"]:
                Details = Incident["first_trigger_log_entry"]["channel"]["details"]
                if Details is not None and "Geneos Event Data" in Details.keys():
                    if "_VARIABLEPATH" in Incident["first_trigger_log_entry"]["channel"]["details"]["Geneos Event Data"]:
                        Geneos_Path = Incident["first_trigger_log_entry"]["channel"]["details"]["Geneos Event Data"]["_VARIABLEPATH"]
                        bGeneosIncidents = True
        #
        DV_Incidents[Incident["id"]] = Incident
        DV_Incidents[Incident["id"]]["Geneos_Path"] = Geneos_Path
        List_Alerts(Incident["id"])
        # QueryAlertParallel(Incident["id"])

if __name__ == "__main__":

    # Starting list for incidents
    Starting_URL = "https://api.pagerduty.com/incidents?statuses%5B%5D=triggered&statuses%5B%5D=acknowledged&time_zone=UTC&include%5B%5D=first_trigger_log_entries&include%5B%5D=assignees&include%5B%5D=acknowledgers&total=true&limit=" + str(Pagination_Limit)

    # Prep response for necessary results
    Incidents_list = pagerduty_session.get(Starting_URL)

    # response.encoding = 'utf-8'
    if Incidents_list.status_code != 202 and Incidents_list.status_code != 200:
        raise ValueError(
            'Request to PagerDuty a server returned an error %s, the response is:\n%s'
            % (Incidents_list.status_code, Incidents_list.text)
            )

    Incidents = Incidents_list.json()
    # print(json.dumps(Incidents, indent=2))

    # Add to the Incident list
    Update_Incident_List(Incidents)

    # print ("----- Entering Loop -----\n")

    # If there are more incidents
    while Incidents["more"]:
        Offset += Pagination_Limit
        Starting_URL += "&offset=" + str(Offset)

        # Run the Incidents query again
        Incidents_list = pagerduty_session.get(Starting_URL)

        # response.encoding = 'utf-8'
        if Incidents_list.status_code != 202 and Incidents_list.status_code != 200:
            raise ValueError(
                'Request to PagerDuty a server returned an error %s, the response is:\n%s'
                % (Incidents_list.status_code, User_List.text)
            )

        Incidents = Incidents_list.json()
        # print(json.dumps(Incidents, indent=2))

        # Add to the Incident list
        Update_Incident_List(Incidents)

    # print ("----- Exit Loop -----\n")

    # Print out column headings
    print("Id, Last Alert, Status, Creation Time, Last Update, Geneos Path, Incident Keys")
    print("<!> Open Incidents, " + str(len(DV_Incidents)))
    for Incident in DV_Incidents:

        # print(json.dumps(Incident, indent=2))
        #Print json response info to the screen
        bGeneosIncidents = False

        # Geneos_Path = "Not Geneos Alert Generated Inicident"
        Geneos_Path = ""

        if "details" in DV_Incidents[Incident]["first_trigger_log_entry"]["channel"]:
            Details = DV_Incidents[Incident]["first_trigger_log_entry"]["channel"]["details"]
            if Details is not None and "Geneos Event Data" in Details.keys():
                if "_VARIABLEPATH" in DV_Incidents[Incident]["first_trigger_log_entry"]["channel"]["details"]["Geneos Event Data"]:
                    Geneos_Path = DV_Incidents[Incident]["first_trigger_log_entry"]["channel"]["details"]["Geneos Event Data"]["_VARIABLEPATH"]
                    bGeneosIncidents = True

        # print row information
        print(DV_Incidents[Incident]["id"] + "," + \
            DV_Incidents[Incident]["alert_summary"] + "," + \
            # DV_Incidents[Incident]["first_trigger_log_entry"]["channel"]["description"] + "," + \
            DV_Incidents[Incident]["status"] + "," + \
            DV_Incidents[Incident]["created_at"] + "," + \
            DV_Incidents[Incident]["last_status_change_at"] + "," + \
            Geneos_Path + "," + \
            DV_Incidents[Incident]["first_trigger_log_entry"]["channel"]["incident_key"])
