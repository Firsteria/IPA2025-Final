from netmiko import ConnectHandler
import re

def get_motd(device_ip):
    username = "admin"
    password = "cisco"

    device_params = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
    }

    try:
        with ConnectHandler(**device_params) as ssh:
            output = ssh.send_command("show running-config", delay_factor=2, max_loops=500)

            # หา banner motd และ delimiter
            match = re.search(r'banner motd (\S+)\n(.*?)\n\1', output, re.DOTALL)
            if match:
                delimiter = match.group(1)
                motd_text = match.group(2)

                # ลบบรรทัดว่างและบรรทัดที่มี delimiter เช่น ^C
                motd_lines = [line for line in motd_text.splitlines() if line.strip() and line.strip() != delimiter]

                # strip whitespace ของแต่ละบรรทัดแล้วรวมกัน
                final_motd = "\n".join([line.strip() for line in motd_lines])

                if final_motd == "":
                    return "Error: No MOTD Configured"
                else:
                    return final_motd
            else:
                return "Error: No MOTD Configured"

    except Exception as e:
        return f"Error: {str(e)}"
