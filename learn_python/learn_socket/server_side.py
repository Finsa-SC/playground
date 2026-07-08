import socket
from concurrent.futures import ThreadPoolExecutor
import threading

class Server:
    def __init__(self):
        self.SERVER = None
        self.PORT = 7070
        self.ADDR = ()
        self.FORMAT = 'utf-8'

        self.clients = set()
        self.lock = threading.Lock()
        self.server = None
        self.resolver = ("8.8.8.8", 80)
        self.executor = ThreadPoolExecutor(max_workers=10)

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_server()

        if exc_type:
            print(f"[CLOSED]")
        return True

    # run socket and make socket reuseable
    def start_server(self) -> None:
        print("[INFO] Starting server...")
        self.ADDR = (self.get_hostname(), self.PORT)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server.bind(self.ADDR)
            self.server.listen()
            print(f"[INFO] Server listening on {self.ADDR[0]}:{self.ADDR[1]}")
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            self.server.close()

    def stop_server(self) -> None:
        print(f"[INFO] Server has been stopped")
        self.server.close()
        self.executor.shutdown(wait=False)

    # Automaticaly figure out local ip and fallback
    def get_hostname(self) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(self.resolver)
                return s.getsockname()[0]
        except:
            print(f"[WARNING] Error occured while trying to resolve host, use {self.SERVER}")
            return socket.gethostbyname(socket.gethostname())

    def connected_client(self, conn, addr):
        try:
            with self.lock:
                self.clients.add(addr)
            print(f"[INFO] New connection made for {addr}, {len(self.clients)} Active connection")
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                text = data.decode(self.FORMAT).strip()

                if not text:
                    break

                print(text)
                self.send_ping(conn)

        except Exception as e:
            print(f"[WARNING] Connection error with {addr}: {e}")
        finally:
            conn.close()
            with self.lock:
                self.clients.discard(addr)
            print(f"[INFO] {addr} has been disconnected, {len(self.clients)} Active connection")

    def client_connect(self):
        try:
            while True:
                conn, addr = self.server.accept()
                self.executor.submit(self.connected_client, conn, addr)
        except OSError:
            print(f"[INFO] Socket closed, stopping client acceptance")

    def run_server(self):
        self.get_hostname()
        self.start_server()
        self.client_connect()
        self.stop_server()

    def send_ping(self, conn):
        message_raw = "PING\n"
        message = message_raw.encode(self.FORMAT)
        conn.send(message)

if __name__ == "__main__":
    with Server() as my_server:
        my_server.run_server()