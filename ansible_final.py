

def motd(ip, message=None, retries=3, delay_seconds=5):
    hosts_file = "hosts"

    # ตรวจสอบ IP
    if ip not in ["10.0.15.61","10.0.15.62","10.0.15.63","10.0.15.64","10.0.15.65"]:
        return f"{ip} Error: Invalid Router IP"

    if message:
        # ตั้งค่า MOTD
        command = [
            "ansible-playbook",
            "-i", hosts_file,
            "playbook.yaml",
            "--extra-vars",
            f"target={ip} motd_message='{message}'"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 and "failed=0" in result.stdout:
            return f"{message} Ok: success"
        else:
            return f"{message} Error: failed"
    else:
        # อ่าน MOTD
        command = [
            "ansible",
            ip,
            "-i", hosts_file,
            "-m", "ios_command",
            "-a",
            "commands='show run | include banner motd'"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout

        # ดึงข้อความ MOTD จริง
        lines = output.splitlines()
        motd_text = []
        capture = False
        for line in lines:
            if "banner motd @" in line:
                capture = True
                continue
            if capture and line.strip() == "@":
                capture = False
                break
            if capture:
                motd_text.append(line.strip())
        if motd_text:
            return " ".join(motd_text)
        else:
            return "Error: No MOTD Configured"
