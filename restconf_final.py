import json
import requests
import sys

requests.packages.urllib3.disable_warnings()


ROUTER_IPS = ["10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"]

headers = {
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")

def get_api_url(ip):
    """สร้าง API URL ตาม IP ที่ระบุ"""
    return f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070119"

def create(ip):
    api_url = get_api_url(ip)
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070119",
            "description": "loopback for 66070119",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [{"ip": "172.1.19.1", "netmask": "255.255.255.0"}]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        return "Cannot create: Interface loopback 66070119"
    elif 200 <= resp.status_code <= 299:
        return "Interface loopback 66070119 is created successfully"
    else:
        return f"Error: Status Code {resp.status_code}"

def delete(ip):
    api_url = get_api_url(ip)
    resp = requests.delete(api_url, auth=basicauth, headers=headers, verify=False)
    if 200 <= resp.status_code <= 299:
        return "Interface loopback 66070119 is deleted successfully"
    elif resp.status_code == 404:
        return "Cannot delete: Interface loopback 66070119"
    else:
        return f"Error: Status Code {resp.status_code}"

def enable(ip):
    api_url = get_api_url(ip)
    yangConfig = {"ietf-interfaces:interface": {"name": "Loopback66070119", "type": "iana-if-type:softwareLoopback", "enabled": True}}
    resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if 200 <= resp.status_code <= 299:
        return "Interface loopback 66070119 is enabled successfully"
    elif resp.status_code == 404:
        return "Cannot enable: Interface loopback 66070119"
    else:
        return f"Error: Status Code {resp.status_code}"

def disable(ip):
    api_url = get_api_url(ip)
    yangConfig = {"ietf-interfaces:interface": {"name": "Loopback66070119", "type": "iana-if-type:softwareLoopback", "enabled": False}}
    resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if 200 <= resp.status_code <= 299:
        return "Interface loopback 66070119 is shutdowned successfully"
    elif resp.status_code == 404:
        return "Cannot shutdown: Interface loopback 66070119"
    else:
        return f"Error: Status Code {resp.status_code}"

def status(ip):
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070119"
    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    if 200 <= resp.status_code <= 299:
        response_json = resp.json()
        admin_status = response_json['ietf-interfaces:interface']['admin-status']
        oper_status = response_json['ietf-interfaces:interface']['oper-status']
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070119 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070119 is disabled"
    elif resp.status_code == 404:
        return "No Interface loopback 66070119"
    else:
        return f"Error: Status Code {resp.status_code}"
