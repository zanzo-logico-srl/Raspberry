import evdev
from evdev import InputDevice, categorize  # import * is evil :)
from logger import multiprocessing, listener_process, listener_configurer, worker_configurer, log_process, logging

dev = InputDevice('/dev/input/event0')

queue = multiprocessing.Queue(-1)
listener = multiprocessing.Process(
    target=listener_process,
    args=(queue, listener_configurer))
listener.start()
worker_configurer(queue)

# print(dev)
log_process(logging.DEBUG, dev)

# for event in dev.read_loop():
#     if event.type == ecodes.EV_KEY:
#         print(categorize(event))

# Provided as an example taken from my own keyboard attached to a Centos 6 box:
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}
rv = ''
start = False
for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        data = evdev.categorize(event)  # Save the event temporarily to introspect it
        if data.keystate == 1:  # Down events only
            key_lookup = scancodes.get(data.scancode) or 'UNKNOWN:{0}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
            # print(logging.DEBUG, 'You Pressed the {0} key!'.format(key_lookup))  # Print it all out!
            log_process(logging.DEBUG, 'You Pressed the {0} key!'.format(key_lookup))

            #return ';0000000000?' #ERROR!
            if (key_lookup == ';'): 
                start = True
                rv = ''
            elif (key_lookup == 'LSHFT'): 
                start = False
                # print(logging.INFO, 'All message is {0} !'.format(rv))  
                log_process(logging.INFO, 'All message is {0} !'.format(rv))
                rv = ''
            else:
                rv += key_lookup



# [ 1192.002930] usb 1-1.3: New USB device found, idVendor=0801, idProduct=0001, bcdDevice= 1.00
# [ 1192.002943] usb 1-1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
# [ 1192.016471] input: HID 0801:0001 as /devices/platform/scb/fd500000.pcie/pci0000:00/0000:00:00.0/0000:01:00.0/usb1/1-1/1-1.3/1-1.3:1.0/0003:0801:0001.0003/input/input2
# [ 1192.086129] hid-generic 0003:0801:0001.0003: input,hidraw0: USB HID v1.01 Keyboard [HID 0801:0001] on usb-0000:01:00.0-1.3/input0

# /dev/input/event0 
