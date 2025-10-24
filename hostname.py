import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://10.0.15.64/restconf/data/Cisco-IOS-XE-native:native/banner/motd"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basicauth = ("admin", "cisco")
resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

if resp.status_code == 200:
    response_json = resp.json()

    # Cisco ส่งข้อมูลในรูปแบบ {"Cisco-IOS-XE-native:motd": {"banner": "@\nAuthorized users only! Managed by 66070119\n@"}}
    motd_raw = response_json.get("Cisco-IOS-XE-native:motd", {}).get("banner", "")

    # ลบเครื่องหมาย '@' และช่องว่างรอบ ๆ
    motd_clean = motd_raw.strip("@").strip()

    if motd_clean:
        print("MOTD:", motd_clean)
    else:
        print("Error: No MOTD Configured")
elif resp.status_code == 404:
    print("Error: No MOTD Configured")
else:
    print("Error:", resp.status_code, resp.text)
