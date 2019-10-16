import http.client
import ssl
import json

PAYLOAD = {
    "filter": {
        "assignee": [
            ".none"
        ],
        "resolution": [
            ".none"
        ],
        "status": [
            ".none"
        ],
        "ticket_id": [
            ".none"
        ]
    },
    "from": 1569317990000,
    "until": 1569339251000
}

API_KEY=""

def restapi():
    try:
        conn = http.client.HTTPSConnection("10.164.53.52", context=ssl._create_unverified_context())
        headers = {
            "accept": "application/json",
            "Authorization": "ExtraHop apikey="+API_KEY,
            "Content-Type": "application/json"
        }
        with open('time.json', 'w') as file:
            until = ""
            payload = json.dumps(PAYLOAD)
            conn.request("POST", "/api/v1/detections/search", headers=headers, body=payload)
            resp = conn.getresponse()
            data = resp.read()
            json_output = json.loads(data)
            for e in json_output:
                id_lookup(e['participants'])

            return json_output
    except http.client.HTTPException as err:
        print("HTTP Error: {0}".format(err))
        return None


def id_lookup(participants):
    try:
        conn = http.client.HTTPSConnection("10.164.53.52", context=ssl._create_unverified_context())
        headers = {
            "accept": "application/json",
            "Authorization": "ExtraHop apikey="+API_KEY,
            "Content-Type": "application/json"
        }
        for people in participants:
            object_id = people['object_id']
            conn.request("GET", f"/api/v1/devices/{object_id}", headers=headers)
            resp = conn.getresponse()
            data = resp.read()
            output = json.loads(data)
            people.update(output)

        return participants

    except http.client.HTTPException as err:
        print(f"Error: {err}")
        return False


restapi()
