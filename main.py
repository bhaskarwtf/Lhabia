from concurrent.futures import ThreadPoolExecutor
import socket
import sys
from core.banner import grab_banner  

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <target_ip> [-p-]")
    sys.exit(1)

ip = sys.argv[1]

scan_all_ports = "-p-" in sys.argv[2:]
start_port = 1
end_port = 65535 if scan_all_ports else 1024

def tcp(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(1.0) 
        result = server.connect_ex((ip, port))
        
        if result == 0:
            
            banner = grab_banner(server, ip, port)
            print(f"[+] Port {port} is open: {banner}")

if __name__ == "__main__":
    print(f"Scanning {ip} from port {start_port} to {end_port}...")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(tcp, range(start_port, end_port + 1))