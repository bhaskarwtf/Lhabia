import socket
from main import ip, start_port, end_port, server

def main(ip, start_port, end_port):
    banner = server.recv(1024).decode().strip()
    
    