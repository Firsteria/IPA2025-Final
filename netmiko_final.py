from netmiko import ConnectHandler
from pprint import pprint
import json

device_ip = "10.0.15.61"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up_count = 0
        down_count = 0
        admin_down_count = 0
        gigabit_interfaces = []
        result = ssh.send_command("show ip int br", use_textfsm=True)
        print(json.dumps(result))
        for interface in result:
            if 'GigabitEthernet' in interface['interface']:
                status = interface.get('status', '')
                interface_name = interface['interface']

                if status == "up":
                    up_count += 1
                    gigabit_interfaces.append(f"{interface_name} up")
                elif status == "down":
                    down_count += 1
                    gigabit_interfaces.append(f"{interface_name} down")
                elif status == "administratively down":
                    admin_down_count += 1
                    gigabit_interfaces.append(f"{interface_name} administratively down")
        ans = ", ".join(gigabit_interfaces)
        ans += f" -> {up_count} up, {down_count} down, {admin_down_count} administratively down"
        return ans

