import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://10.0.15.63/restconf/data/Cisco-IOS-XE-native:native/hostname"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basicauth = ("admin", "cisco")
resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

if resp.status_code == 200:
    response_json = resp.json()
    hostname = response_json.get("Cisco-IOS-XE-native:hostname")
    print("Hostname:", hostname)
else:
    print("Error:", resp.status_code, resp.text)
