from scapy.all import *
import random

class SynScanner:

    @staticmethod
    def scan(ip, port):

        src_port = random.randint(1024, 65535)

        packet = IP(dst=ip) / TCP(
            sport=src_port,
            dport=port,
            flags='S'
        )

        response = sr1(packet, timeout=1, verbose=0)

        if response is None:
            return "Filtered"

        if response.haslayer(TCP):

            flags = response[TCP].flags

            # SYN-ACK
            if flags == 0x12:

                rst_packet = IP(dst=ip) / TCP(
                    sport=src_port,
                    dport=port,
                    flags='R'
                )

                send(rst_packet, verbose=0)

                return "Open"

            # RST-ACK
            elif flags == 0x14:
                return "Closed"

        return "Unknown"
    
    
    