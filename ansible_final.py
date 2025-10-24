import subprocess
import time  # ต้อง import time เพื่อใช้หน่วงเวลา

def showrun(retries=3, delay_seconds=5):
    command = ['ansible-playbook', 'playbook.yaml']
    
    for attempt in range(retries):
        print(f"--- Attempt {attempt + 1} of {retries} ---")
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            print("=== Ansible stdout ===")
            print(result.stdout)
            print("=== Ansible stderr ===")
            print(result.stderr)

            # 1. ตรวจสอบว่า Ansible รันสำเร็จหรือไม่ (returncode == 0)
            if result.returncode == 0:
                # 2. ถ้าสำเร็จ, ตรวจสอบ output ว่าตรงตามที่คาดหวังหรือไม่
                if 'ok=2' in result.stdout or 'ok=1' in result.stdout:
                    print("Ansible run successful.")
                    return 'show_run_66070119_R1-Exam.txt'  # สำเร็จ ออกจากฟังก์ชันเลย
                else:
                    print("Error: Ansible output unexpected.")
                    # อาจจะไม่ต้อง retry ถ้า output ผิด แต่เราจะลองใหม่เผื่อไว้
            else:
                # 3. ถ้า Ansible ล้มเหลว (เช่น router ต่อไม่ติด)
                print(f"Ansible failed with code {result.returncode}. Retrying...")

        except FileNotFoundError:
            print("=== Python Error ===")
            print("Error: 'ansible-playbook' command not found. Cannot retry.")
            return "Error: Ansible executable not found" # Lỗi นี้แก้ด้วย retry ไม่ได้
        except Exception as e:
            print(f"=== Python Error ===")
            print(f"An unexpected error occurred: {e}")
            # Lỗi อื่นๆ อาจจะลอง retry

        # ถ้ายังไม่สำเร็จ และยังไม่ครบจำนวนครั้ง ให้หน่วงเวลา
        if attempt < retries - 1:
            print(f"Waiting {delay_seconds} seconds before next attempt...")
            time.sleep(delay_seconds)

    # ถ้าวน loop ครบ 3 ครั้งแล้วยังไม่สำเร็จ
    print("All retry attempts failed.")
    return "Error: Ansible failed after all retries"