from concurrent.futures import ThreadPoolExecutor
import socket

from core.argprase import parse_arguments
from core.banner import grab_banner
from scanners.syn import SynScanner

args = parse_arguments()
ip = args.ip
scan_type = "-sT" if args.tcp_connect else "-sS" if args.syn_scan else "-sV" if args.version_detection else None
scan_all_ports = args.p == "1-65535"


start_port = 1
end_port = 65535 if scan_all_ports else 1024


def tcp_scan(port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        server.settimeout(1.0)

        result = server.connect_ex((ip, port))

        if result == 0:
            if scan_type == "-sV":
                banner = grab_banner(server, ip, port)
                print(f"[+] Port {port} open with {banner}")
            else:
                print(f"[TCP] Port {port} open")


def syn_scan(port):

    result = SynScanner.scan(ip, port)
    
    if result == "Open":
        print(f"[SYN] Port {port} open")
    elif result == "Closed":
        print(f"[SYN] Port {port} closed")
    elif result == "Filtered":
        print(f"[SYN] Port {port} filtered")


if __name__ == "__main__":

    print(f"Scanning {ip} from {start_port} to {end_port}")

    with ThreadPoolExecutor(max_workers=100) as executor:

        if scan_type == "-sT":
            executor.map(tcp_scan, range(start_port, end_port + 1))
        elif scan_type == "-sS":
            executor.map(syn_scan, range(start_port, end_port + 1))
        elif scan_type == "-sV":
            executor.map(tcp_scan,range(start_port,end_port +1))

        else:
            print("Invalid scan type")