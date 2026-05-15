import socket 

ip = str(input("Tell me the target ip??")) 
port = 0
end_port = 1023
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(port, end_port):
   
   port += 1
   rel = server.connect_ex((ip, port))
   if rel == 0:
      print(f"Port is open {port}")
   