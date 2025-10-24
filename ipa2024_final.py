#######################################################################################
# Yourname: ปิยะภัทร ไชยวรรณะ
# Your student ID: 660701119
# Your GitHub Repo: https://github.com/Firsteria/IPA2024-Final.git
#######################################################################################

import requests
import json
import restconf_final
import netconf_final
import ansible_final
from dotenv import load_dotenv
import os
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv()

ACCESS_TOKEN = os.environ.get("accesstoken")
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNmZmMmNhMTAtYWI5My0xMWYwLTlhNzItZWZmOGEyMzcyMDc3"

selected_method = None  # เก็บ method ระหว่างคำสั่ง

while True:
    time.sleep(1)
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}
    getHTTPHeader = {"Authorization": ACCESS_TOKEN}

    r = requests.get("https://webexapis.com/v1/messages", params=getParameters, headers=getHTTPHeader)
    if not r.status_code == 200:
        raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")

    json_data = r.json()
    if len(json_data["items"]) == 0:
        continue  # ไม่มีข้อความใหม่

    message = json_data["items"][0]["text"]
    print("Received message:", message)

    if message.startswith("/66070119"):
        parts = message.split(" ")

        # --- ถ้าไม่มีอะไรมากกว่า /66070123 ---
        if len(parts) == 1:
            responseMessage = "Error: No method specified"

        # --- ถ้าใส่ method อย่างเดียว ---
        elif len(parts) == 2:
            second = parts[1].lower()
            if second == "restconf":
                selected_method = "restconf"
                responseMessage = "Ok: Restconf"
            elif second == "netconf":
                selected_method = "netconf"
                responseMessage = "Ok: Netconf"
            elif second.count(".") == 3:
                responseMessage = "Error: No command found."
            elif second in ["create","delete","enable","disable","status"]:
                responseMessage = "Error: No IP specified"
            else:
                responseMessage = "Error: No method specified"

        # --- ถ้าใส่ IP + action ---
        elif len(parts) >= 3:
            ip = parts[1]
            action = parts[2].lower()

            # --- ถ้ายังไม่เลือก method ก่อนหน้า ---
            if selected_method is None:
                responseMessage = "Error: No method specified"
            else:
                # เลือก library ตาม method
                lib = restconf_final if selected_method == "restconf" else netconf_final

                if action == "create":
                    responseMessage = lib.create(ip) + f" using {selected_method.capitalize()}"
                elif action == "delete":
                    responseMessage = lib.delete(ip) + f" using {selected_method.capitalize()}"
                elif action == "enable":
                    responseMessage = lib.enable(ip) + f" using {selected_method.capitalize()}"
                elif action == "disable":
                    responseMessage = lib.disable(ip) + f" using {selected_method.capitalize()}"
                elif action == "status":
                    responseMessage = lib.status(ip) + f" (checked by {selected_method.capitalize()})"
                else:
                    responseMessage = "Error: No command found."

        # --- ส่งข้อความกลับ Webex ---
        postData = json.dumps({"roomId": roomIdToGetMessages, "text": responseMessage})
        HTTPHeaders = {"Authorization": ACCESS_TOKEN, "Content-Type": "application/json"}

        r = requests.post("https://webexapis.com/v1/messages", data=postData, headers=HTTPHeaders)
        if not r.status_code == 200:
            raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")
