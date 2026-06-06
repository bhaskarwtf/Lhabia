import argparse
def parse_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("ip", help="Target IP address")
    arg_parser.add_argument("-sT","--tcp-connect", help="TCP Connect Scan", action="store_true")
    arg_parser.add_argument("-sS","--syn-scan", help="SYN Scan", action="store_true")
    arg_parser.add_argument("-p", help="Port range (e.g., 1-1000)", default="1-1024")
