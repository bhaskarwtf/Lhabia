import socket
import ssl

def grab_banner(connected_socket, ip, port):
    
    try:
        banner = connected_socket.recv(1024).decode(errors='ignore').strip()
        if banner:
            return banner
    except Exception:
        pass

    if port in [80, 8080]:
        return grab_http_banner(ip, port)
    if port in [443, 8443]:
        return https_grabber(ip, port)
    if port in [3306, 5432, 1433]:
        return my_sql_grabber(ip, port)
    if port in [5432]:
        return postgre_sql_grabber(ip, port)

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
    except Exception:
        return "HTTP open (Request failed)"


def https_grabber(ip, port):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((ip, port))

            with context.wrap_socket(sock, server_hostname=ip) as tls_sock:
                tls_sock.settimeout(5)
                ssl_request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: NetScanner/1.0\r\nConnection: close\r\n\r\n"
                tls_sock.sendall(ssl_request.encode())

                ssl_response = tls_sock.recv(2048).decode(errors='ignore')

                for line in ssl_response.split("\r\n"):
                    if line.lower().startswith("server:"):
                        return f"HTTPS Server: {line.split(':', 1)[1].strip()}"
                return "HTTPS open (Server header missing)"
    except Exception:
        return "HTTPS open (Request failed)"
    
def my_sql_grabber(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sql_sock:
            sql_sock.settimeout(1.5)
            sql_sock.connect((ip, port))

            sql_request = b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
            sql_sock.sendall(sql_request)

            response = sql_sock.recv(2048).decode(errors='ignore')

            if response:
                return f"SQL Service: {response.strip()}"
            else:
                return "SQL open (No response)"
    except Exception:
        return "SQL open (Request failed)"  

def postgre_sql_grabber(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sql_sock:
            sql_sock.settimeout(1.5)
            sql_sock.connect((ip, port))

            sql_request = b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
            sql_sock.sendall(sql_request)

            response = sql_sock.recv(2048).decode(errors='ignore')

            if response:
                return f"PostgreSQL Service: {response.strip()}"
            else:
                return "PostgreSQL open (No response)"
    except Exception:
        return "PostgreSQL open (Request failed)"

def redis_grabber(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as redis_sock:
            redis_sock.settimeout(1.5)
            redis_sock.connect((ip, port))

            redis_request = b"*1\r\n$4\r\nINFO\r\n"
            redis_sock.sendall(redis_request)

            response = redis_sock.recv(2048).decode(errors='ignore')

            if response:
                return f"Redis Service: {response.strip()}"
            else:
                return "Redis open (No response)"
    except Exception:
        return "Redis open (Request failed)"

    