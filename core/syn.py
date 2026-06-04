from scapy.all import *

class syn:
    def syn(ip,port):
        src_port = random.randint(1024,65535)

        packet = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='S')
        response = sr1(packet, timeout=1, verbose=0)

        if response is None:
            return "Filtered"
        
        elif response.haslayer(TCP):
            if response[TCP].flags == '0x12':
                rest_packet = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='R')
                send(rest_packet, verbose=0)
                
                return "Open"
            
        elif response[TCP].flags == '0x14':
                return "Closed"
            
        return "Unknown"
    


    
    
    