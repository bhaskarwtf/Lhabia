import argparse
def parse_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("ip", help="Target IP address")
    arg_parser.add_argument("-sT","--tcp-connect", help="TCP Connect Scan", action="store_true")
    arg_parser.add_argument("-sS","--syn-scan", help="SYN Scan", action="store_true")
    arg_parser.add_argument("-sV","--version-detection", help="Version Detection", action="store_true")
    arg_parser.add_argument("-fC","--full-scan", help="Full port scan Upto 65535", action="store_true")
    return arg_parser.parse_args()
