import sys
import pywinusb.hid as hid
import time
import argparse
from argparse import RawTextHelpFormatter

description_string = """Simple program for testing USB HID devices
Examples:
python hid_tester.py -list
python hid_tester.py -receive -pid 22352 -timeout 10
python hid_tester.py -send -pid 22352 -rid 2 -data 01
"""

parser = argparse.ArgumentParser(description=description_string, formatter_class=RawTextHelpFormatter)
parser.add_argument('-list', action='store_true', help='List all connected USB HID devices')
parser.add_argument('-send', action='store_true', help='Send report with specified ID to device with specified PID. –rid, -pid, -data options reqired')
parser.add_argument('-receive', action='store_true', help='List all connected USB HID devices')
parser.add_argument('-rid', help='Report ID in hex')
parser.add_argument('-pid', help='PID of target device')
parser.add_argument('-data', help='Data to be sent in hex string')
parser.add_argument('-timeout', help='Print reports from specified device during specified timeout. –rid and –timeout parameters required')

args = parser.parse_args()

# Launched with no arguments
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

# Handler for received data
def rx_handler(data):
    print('Got data: ', data)

# List all devices
all_devices = hid.find_all_hid_devices()
num_devices = len(all_devices)
if args.list:
    print(num_devices, "devices found")

for device in all_devices:
    if args.list:
        # Print device information
        print("{} {}".format(device.vendor_name, device.product_name))
        print("  VID: {}".format(device.vendor_id))
        print("  PID: {}".format(device.product_id))
        try:
            device.open()
            print("  Input reports")
            for report in device.find_input_reports():
                print("    {}".format(report))
            print("  Output reports")
            for report in device.find_output_reports():
                print("    {}".format(report))
        finally:
            device.close()
    
    if args.pid == None:
        continue
    
    if int(args.pid) == device.product_id:
        if args.receive:
            # Receive data from device
            if args.timeout == None:
                print("Please set -timeout argument")
                exit(-1)
            try:
                device.open()
                print("Wait {} s for some data".format(int(args.timeout)))
                device.set_raw_data_handler(rx_handler)
                time.sleep(int(args.timeout))
            finally:
                device.close()

        if args.send:
            # Send data to device
            if args.rid == None:
                print("Please set report ID via -rid argument")
                exit(-1)
                
            if args.rid == None:
                print("Please set -data argument")
                exit(-1)
                
            try:
                device.open()
                for report in device.find_output_reports():
                    raw_report_data = report.get_raw_data()
                    if raw_report_data[0] != int(args.rid, 16):
                        continue
                    
                    data_to_send = bytes.fromhex(args.data)
                    raw_report_data = [raw_report_data[0]]
                    for b in data_to_send:
                        raw_report_data.append(b)
                    report.set_raw_data(raw_report_data)
                    report.send()
                    exit(0)
                    
                print("Report with specefied ID not found")
                exit(-1)
                        
            finally:
                device.close()      
