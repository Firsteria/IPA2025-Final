#######################################################################################
# Yourname: ปิยะภัทร ไชยวรรณะ
# Your student ID: 660701119
# Your GitHub Repo: https://github.com/Firsteria/IPA2024-Final.git
#######################################################################################

import requests
import json
import restconf_final
from dotenv import load_dotenv
import os
import time
import netmiko_final
import ansible_final
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv()

ACCESS_TOKEN = os.environ.get("accesstoken")
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNmZmMmNhMTAtYWI5My0xMWYwLTlhNzItZWZmOGEyMzcyMDc3"

while True:
    time.sleep(1)
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}
    getHTTPHeader = {"Authorization": ACCESS_TOKEN}

    r = requests.get("https://webexapis.com/v1/messages", params=getParameters, headers=getHTTPHeader)
    if not r.status_code == 200:
        raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")

    json_data = r.json()
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    message = json_data["items"][0]["text"]
    print("Received message:", message)

    message = json_data["items"][0]["text"]
    print("Received message:", message)

    if message.startswith("/66070119"):
        parts = message.split(" ")

        if len(parts) == 1:
            responseMessage = "Error: No method specified"

        elif len(parts) == 2:
            second = parts[1]

            if second in ["create", "delete", "enable", "disable", "status"]:
                responseMessage = "Error: No IP specified"
            elif second.count(".") == 3:
                responseMessage = "Error: No command found."
            elif second == "restconf":
                responseMessage = "Ok: Restconf"
            else:
                responseMessage = "Error: No method specified"

        elif len(parts) >= 3:
            ip = parts[1]
            action = parts[2]

            if action == "create":
                responseMessage = restconf_final.create(ip)
            elif action == "delete":
                responseMessage = restconf_final.delete(ip)
            elif action == "enable":
                responseMessage = restconf_final.enable(ip)
            elif action == "disable":
                responseMessage = restconf_final.disable(ip)
            elif action == "showrun":
                filename = ansible_final.showrun()
                if filename and filename.endswith(".txt"):
                    responseMessage = "ok"
                else:
                    responseMessage = filename or "Error: No file created"
            else:
                responseMessage = "Error: No method specified"

        # ✅ ส่งกลับ Webex
        if 'action' in locals() and action == "showrun" and responseMessage == "ok":
            with open(filename, "rb") as fileobject:
                postData = MultipartEncoder(
                    fields={
                        "roomId": roomIdToGetMessages,
                        "text": "show running config",
                        "files": (os.path.basename(filename), fileobject, "text/plain"),
                    }
                )
                HTTPHeaders = {
                    "Authorization": ACCESS_TOKEN,
                    "Content-Type": postData.content_type,
                }
        else:
            postData = json.dumps({"roomId": roomIdToGetMessages, "text": responseMessage})
            HTTPHeaders = {"Authorization": ACCESS_TOKEN, "Content-Type": "application/json"}

        r = requests.post("https://webexapis.com/v1/messages", data=postData, headers=HTTPHeaders)
        if not r.status_code == 200:
            raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")

    # ❌ ถ้า message ไม่ใช่ /66070119 → จะไม่ประกาศ responseMessage และไม่ส่งอะไรกลับ
