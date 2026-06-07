from scapy.all import IP, TCP, sr1, send
import random
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class SynScanner:

    @staticmethod
    def scan(ip, port):

        src_port = random.randint(1024, 65535)

        packet = IP(dst=ip) / TCP(
            sport=src_port,
            dport=port,
            flags="S",
            seq=random.randint(0, 4294967295)
        )

        response = sr1(packet, timeout=4, retry=1, verbose=0)

        if response is None:
            return "Filtered"

        if response.haslayer(TCP):

            flags = response[TCP].flags

            if flags == 0x12:

                rst_packet = IP(dst=ip) / TCP(
                    sport=src_port,
                    dport=port,
                    flags="R",
                    seq=response[TCP].ack
                )

                send(rst_packet, verbose=0)

                return "Open"
            elif flags == 0x14:
                return None 

        return "Unknown"