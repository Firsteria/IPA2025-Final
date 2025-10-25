#######################################################################################
# Yourname: ปิยะภัทร ไชยวรรณะ
# Your student ID: 66070119
# Your GitHub Repo: https://github.com/Firsteria/IPA2025-Final.git
#######################################################################################

import requests
import json
import time
import os
from dotenv import load_dotenv

import ansible_final
import netmiko_final
import restconf_final
import netconf_final

load_dotenv()
ACCESS_TOKEN = os.environ.get("accesstoken")
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vYmQwODczMTAtNmMyNi0xMWYwLWE1MWMtNzkzZDM2ZjZjM2Zm"

selected_method = None

def send_webex_message(room_id, message):
    postData = json.dumps({"roomId": room_id, "text": message})
    HTTPHeaders = {"Authorization": ACCESS_TOKEN, "Content-Type": "application/json"}
    r = requests.post("https://webexapis.com/v1/messages", data=postData, headers=HTTPHeaders)
    if not r.status_code == 200:
        raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")

while True:
    time.sleep(1)

    
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}
    getHTTPHeader = {"Authorization": ACCESS_TOKEN}
    r = requests.get("https://webexapis.com/v1/messages", params=getParameters, headers=getHTTPHeader)
    if r.status_code != 200:
        raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")

    json_data = r.json()
    if len(json_data["items"]) == 0:
        continue  

    message = json_data["items"][0]["text"]
    print("Received message:", message)

    if message.startswith("/66070119"):
        parts = message.split(" ")

        
        if len(parts) == 1:
            responseMessage = "Error: No method specified"

        
        elif len(parts) == 2:
            second = parts[1].lower()
            if second in ["restconf", "netconf"]:
                selected_method = second
                responseMessage = f"Ok: {second.capitalize()}"
            elif second.count(".") == 3:  
                if selected_method is None:
                    responseMessage = "Error: No method specified"
                else:
                    responseMessage = "Error: No command found."
            elif second in ["create", "delete", "enable", "disable", "status"]:  # action แต่ยังไม่ได้ IP
                if selected_method is None:
                    responseMessage = "Error: No method specified"
                else:
                    responseMessage = "Error: No IP specified"
            else:
                responseMessage = "Error: No method specified"

        
        elif len(parts) >= 3:
            ip = parts[1]
            action = parts[2].lower()

            
            if action == "motd":
                motd_message = " ".join(parts[3:]) if len(parts) > 3 else None

                if motd_message:
                    
                    result = ansible_final.motd(ip, motd_message)
                    responseMessage = result  
                else:
                    
                    result = netmiko_final.get_motd(ip)
                    responseMessage = result  

            else:
                
                if selected_method is None:
                    responseMessage = "Error: No method specified"
                else:
                    lib = restconf_final if selected_method == "restconf" else netconf_final

                    if action == "create":
                        result = lib.create(ip)
                    elif action == "delete":
                        result = lib.delete(ip)
                    elif action == "enable":
                        result = lib.enable(ip)
                    elif action == "disable":
                        result = lib.disable(ip)
                    elif action == "status":
                        result = lib.status(ip)
                    else:
                        result = "Error: No command found"

                    
                    if result.startswith("Error") or result.startswith("Cannot"):
                        responseMessage = result
                    else:
                        responseMessage = f"{result} using {selected_method.capitalize()}"

       
        send_webex_message(roomIdToGetMessages, responseMessage)
