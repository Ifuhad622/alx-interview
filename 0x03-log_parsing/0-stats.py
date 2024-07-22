#!/usr/bin/python3
"""
A script that reads stdin line by line and computes metrics.
"""

import sys
import signal

# Initialize variables
total_size = 0
status_codes_count = {
    '200': 0,
    '301': 0,
    '400': 0,
    '401': 0,
    '403': 0,
    '404': 0,
    '405': 0,
    '500': 0
}
line_count = 0

def print_stats():
    """
    Print accumulated metrics
    """
    print(f"File size: {total_size}")
    for code in sorted(status_codes_count.keys()):
        if status_codes_count[code] > 0:
            print(f"{code}: {status_codes_count[code]}")

def signal_handler(sig, frame):
    """
    Signal handler for keyboard interruption (CTRL + C)
    """
    print_stats()
    sys.exit(0)

# Set up signal handler
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        try:
            parts = line.split()
            if len(parts) < 9:
                continue

            file_size = int(parts[-1])
            status_code = parts[-2]

            total_size += file_size
            if status_code in status_codes_count:
                status_codes_count[status_code] += 1

            line_count += 1

            if line_count % 10 == 0:
                print_stats()
        except Exception as e:
            pass
except KeyboardInterrupt:
    print_stats()
    raise
