import socket

def grab_banner(connected_socket, ip, port):
    
    try:
        banner = connected_socket.recv(1024).decode(errors='ignore').strip()
        if banner:
            return banner
    except Exception:
        pass  

    if port in [80, 8080, 443]:  
        return grab_http_banner(ip, port)

    return "TCP open (No banner received)"


def grab_http_banner(ip, port):
    
    try:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as http_sock:
            http_sock.settimeout(1.5)
            http_sock.connect((ip, port))
            

            http_request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: NetScanner/1.0\r\nConnection: close\r\n\r\n"
            http_sock.sendall(http_request.encode())
            
            
            response = http_sock.recv(2048).decode(errors='ignore')
            

            for line in response.split("\r\n"):
                if line.lower().startswith("server:"):
                    return f"HTTP Server: {line.split(':', 1)[1].strip()}"
                    
            return "HTTP open (Server header missing)"
    except Exception as e:
        return f"HTTP open (Request failed)"