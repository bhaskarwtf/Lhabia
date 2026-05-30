from concurrent.futures import ThreadPoolExecutor
import socket
import sys
from core.banner import main

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <target_ip>")
    sys.exit(1)

ip = sys.argv[1]
second_command = sys.argv[2] if len(sys.argv) > 2 else None
third_command = sys.argv[3] if len(sys.argv) > 3 else None
start_port = 0
end_port = 1024

def tcp(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(0.5)
        rel = server.connect_ex((ip, port))
        if rel == 0:
                print(f"Port is open {port}: {main(banner)}")

if second_command == "-p-" or third_command == "-p-":
     end_port = 65535

with ThreadPoolExecutor(max_workers=100) as executor:
           executor.map(tcp, range(start_port, end_port))
    
