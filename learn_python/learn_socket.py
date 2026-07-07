import socket

HOST_NAME = socket.gethostname()
print(f"Hostname: {HOST_NAME}")

HOST = socket.gethostbyname(HOST_NAME)
print(f"Host: {HOST}")

ADDR = (HOST, 5050)
print(f"ADDR: {ADDR}\n\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

s.listen()
print(f"[INFO] Server is listening on {ADDR[0]}:{ADDR[1]}")
print("[INFO] Waiting request...")
conn, addr = s.accept()

print("[INFO] Connected")
print(f"Connection={conn}\n Address={addr}")

while True:
    data = conn.recv(1024)

    if not data.strip():
        print("[CLOSED] Connection closed")
        break

    print(data)
    conn.send(b"Hello\n")

conn.close()
s.close()