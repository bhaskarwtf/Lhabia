from scapy.all import IP, TCP, send, AsyncSniffer
import random
import time


class SynScanner:

    def __init__(self, target_ip, ports, timeout=3, rate=1000):

        self.target_ip = target_ip
        self.ports = ports
        self.timeout = timeout
        self.rate = rate

        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []

        self.sent_ports = set()
        self.responded_ports = set()

    def packet_handler(self, packet):

        if packet.haslayer(TCP):

            tcp = packet[TCP]

            src_port = tcp.sport
            flags = tcp.flags

            if src_port not in self.sent_ports:
                return

            self.responded_ports.add(src_port)

            # SYN + ACK = OPEN
            if flags == 0x12:

                self.open_ports.append(src_port)

                rst_packet = IP(dst=self.target_ip) / TCP(
                    dport=src_port,
                    sport=random.randint(1024, 65535),
                    flags="R",
                    seq=tcp.ack
                )

                send(rst_packet, verbose=0)

            # RST + ACK = CLOSED
            elif flags == 0x14:
                self.closed_ports.append(src_port)

    def send_syn_packets(self):

        counter = 0

        for port in self.ports:

            packet = IP(dst=self.target_ip) / TCP(
                sport=random.randint(1024, 65535),
                dport=port,
                flags="S",
                seq=random.randint(0, 4294967295)
            )

            send(packet, verbose=0)

            self.sent_ports.add(port)

            counter += 1

            # rate limiting
            if counter >= self.rate:
                time.sleep(1)
                counter = 0

    def scan(self):

        print(f"[*] Starting SYN scan on {self.target_ip}")

        sniffer = AsyncSniffer(
            filter=f"tcp and host {self.target_ip}",
            prn=self.packet_handler,
            store=False
        )

        sniffer.start()

        start_time = time.time()

        self.send_syn_packets()

        time.sleep(self.timeout)

        sniffer.stop()

        # anything without response = filtered
        for port in self.sent_ports:

            if port not in self.responded_ports:
                self.filtered_ports.append(port)

        end_time = time.time()

        self.print_results(end_time - start_time)

    def print_results(self, elapsed):

        for port in sorted(self.open_ports):
            print(f"[OPEN] Port {port}")

        for port in sorted(self.closed_ports):
            print(f"[CLOSED] Port {port}")

        for port in sorted(self.filtered_ports):
            print(f"[FILTERED] Port {port}")

        print(f"\nScanned {len(self.sent_ports)} ports in {elapsed:.2f} seconds")