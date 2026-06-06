from scapy.all import IP, TCP, sr, send
import random

class SynScanner:

    @staticmethod
    def scan(ip, port):

        src_port = random.randint(1024, 65535)

        packet = IP(dst=ip) / TCP(
            sport=src_port,
            dport=port,
            flags='S',
            seq=random.randint(0, 4294967295)
        )

        
        response = sr(packet, timeout=2, verbose=0)
        if not response:
            return "Filtered"  


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
