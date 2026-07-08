import socket
from concurrent.futures import ThreadPoolExecutor
import threading


class MyServer:
    def __init__(self):
        self.SERVER = None
        self.PORT = 12562
        self.ADDRESS = None
        self.FORMAT = 'utf-8'

        self.clients = set()
        self.lock = threading.Lock()
        self.server_socket = None
        self.resolver = "8.8.8.8"
        self.executor = ThreadPoolExecutor(max_workers=10)

    # Context manager
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_server()
        self.executor.shutdown(wait=False)

        if exc_type:
            print(f"[ERROR] {exc_type}")
        return True

    # Start the server to listening
    def start_server(self) -> None:
        print("[INFO] Starting server...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(self.ADDRESS)
            server.listen()
            self.server_socket = server
            print(f"[SUCCESS] Server started successfully\n[INFO] Server listening on {self.SERVER}:{self.PORT}")
        except Exception as e:
            server.close()
            print(f"[ERROR] Failed to run the server: {e}")

    def stop_server(self) -> None:
        if self.server_socket:
            self.server_socket.close()
            print("[SUCCESS] Server has been stopped")

    # Resolve local ip address with make connection to dns resolver and get the sock name
    def get_hostname(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                resolver_addr = (self.resolver, 80)
                s.connect(resolver_addr)
                self.SERVER = s.getsockname()[0]
                print(f"[INFO] Success resolve hostname from {self.resolver}: {self.SERVER}")
        except Exception:
            self.SERVER = socket.gethostbyname(socket.gethostname())
            print(f"[ERROR]: Error occured while trying to resolve host, use {self.SERVER} instead")
        self.ADDRESS = (self.SERVER, self.PORT)

    def connecting_client(self, conn, addr):
        with self.lock:
            self.clients.add(addr)
            print(f"[INFO] New connection has been created with {addr}, total connected: {len(self.clients)}")

        try:
            while True:
                data = conn.recv(1024)

                if not data:
                    break

                text = data.decode(self.FORMAT).strip()

                if "exit" in text.lower():
                    break
                print(data.decode(self.FORMAT))
        except Exception as e:
            print(f"[WARNING] Connection error with {addr}: {e}")
        finally:
            with self.lock:
                self.clients.discard(addr)
                print(f"[INFO] {addr} disconnected, total connected: {len(self.clients)}")
            conn.close()

    def client_connect(self):
        try:
            while True:
                conn, addr = self.server_socket.accept()
                self.executor.submit(self.connecting_client, conn, addr)
        except OSError:
            print(f"[INFO] Socket closed, stopping client acceptance")

    def run_server(self):
        self.get_hostname()
        self.start_server()

        try:
            self.client_connect()
        except KeyboardInterrupt:
            print("[INFO] Server shutting down by user...")


with MyServer() as my_server:
    my_server.run_server()

# my_server.get_hostname()
# my_server.start_server()
# my_server.stop_server()