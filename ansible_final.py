import subprocess

# Mapping IP → hostname ตามไฟล์ hosts ของ Ansible
ip_to_name = {
    "10.0.15.61": "IPA-Router1",
    "10.0.15.62": "IPA-Router2",
    "10.0.15.63": "IPA-Router3",
    "10.0.15.64": "IPA-Router4",
    "10.0.15.65": "IPA-Router5"
}

def motd(ip, message=None):
    """
    ใช้ Ansible เพื่อ configure หรืออ่าน MOTD บน router
    ip: ตัวอย่าง 10.0.15.61
    message: ถ้าไม่ None → config MOTD, ถ้า None → อ่าน MOTD
    """
    host_name = ip_to_name.get(ip)
    if not host_name:
        return f"Error: Host {ip} not found in inventory"

    # extra-vars ให้ playbook รู้ว่า configure หรืออ่าน
    extra_vars = f"motd_message='{message}' configure={'true' if message else 'false'}"

    command = [
        "ansible-playbook",
        "playbook.yaml",  # ใช้ playbook สำหรับ MOTD
        "--limit", host_name,
        "--extra-vars", extra_vars
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        # ถ้า ansible มี error
        if result.returncode != 0:
            return f"Error: Ansible failed\n{result.stderr}"

        # parse stdout หา result_message:
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("result_message:"):
                # คืนค่า string หลัง "result_message:"
                return line.split(":", 1)[1].strip()

        # ถ้าไม่เจอ
        return "Error: Unable to parse result"

    except Exception as e:
        return f"Error: {e}"
