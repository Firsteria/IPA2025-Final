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

    if message.startswith("/66070119"):
        command = message.split(" ", 1)[1]
        print("Command:", command)

        if command == "create":
            responseMessage = restconf_final.create()
        elif command == "delete":
            responseMessage = restconf_final.delete()
        elif command == "enable":
            responseMessage = restconf_final.enable()
        elif command == "disable":
            responseMessage = restconf_final.disable()
        elif command == "status":
            responseMessage = restconf_final.status()
        elif command == "gigabit_status":
            responseMessage = netmiko_final.gigabit_status()
        elif command == "showrun":
            filename = ansible_final.showrun()
            if filename and filename.endswith(".txt"):
                responseMessage = "ok"
            else:
                responseMessage = filename or "Error: No file created"
        else:
            responseMessage = "Error: No command or unknown command"

        # ✅ Post back to Webex
        if command == "showrun" and responseMessage == "ok":
            fileobject = open(filename, "rb")
            filetype = "text/plain"
            postData = MultipartEncoder(
                fields={
                    "roomId": roomIdToGetMessages,
                    "text": "show running config",
                    "files": (os.path.basename(filename), fileobject, filetype),
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
