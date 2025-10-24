import subprocess

def motd(ip, message):
    hosts_file = "hosts"
    command = [
        "ansible-playbook",
        "-i", hosts_file,
        "playbook.yaml",
        "--extra-vars",
        f"target={ip} motd_message='{message}'"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print("=== Ansible stdout ===")
        print(result.stdout)

        if result.returncode == 0 and "failed=0" in result.stdout:
            return "Ok: success"
        else:
            return "Error: failed"
    except FileNotFoundError:
        return "Error: ansible-playbook not found"
