from concurrent.futures import ThreadPoolExecutor
import socket
import sys

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <target_ip>")
    sys.exit(1)

ip = sys.argv[1]


def tcp(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(0.5)
        rel = server.connect_ex((ip, port))
        if rel == 0:
            try:
                banner = server.recv(1024).decode().strip()
                print(f"Port is open {port} : {banner}")
            except socket.timeout:
                print(f"Port is open {port}")
        



with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(tcp, range(0, 1024))
    
