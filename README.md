# Hid tester

Simple command line application for debugging Custom USB HID devices.

## Usage

Help:
`python hid_tester.py -h`

List all available Custom USB HID devices:
`python hid_tester.py -list`

Listen reports from the device with specified PID:
`python hid_tester.py -receive -pid <PID> -timeout <Timeout in seconds>`

Send data to the device with specifies PID:
`python hid_tester.py -send -pid <PID> -rid <Report ID> -data <Data in hex format>`
