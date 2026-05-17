import socket
import time
import sys

ip=sys.argv[1]

if len(sys.argv) < 2:
    print("Usage: python3 main.py <ip>")
    sys.exit()
    
start_port = 0
end_port = 1023


def tcp():
    print("Starting TCP scan .....")
    time.sleep(5)
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.settimeout(0.5)
            rel = server.connect_ex((ip, port))
            if rel == 0:
                print(f"Port is open {port}")


if __name__ == "__main__":
    tcp()