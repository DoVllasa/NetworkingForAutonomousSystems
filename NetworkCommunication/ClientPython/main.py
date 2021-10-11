# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import json

def main():
    device = XBeeDevice('/dev/tty.usbserial-AC00J708', 9600)
    device.open()

    destination = 'D6F2DF74D'
    source = device.get_bluetooth_mac_addr()

    packet = {
        'objectType': 0,
        'source': source,
        'destination': destination,
        'identifier': str(source) + destination,
    }

    device.send_data_broadcast(json.dumps(packet))

    while True:
        msg = device.read_data()
        if msg:
            packet = json.loads(msg.data)
            objectType = packet['objectType']
            if (objectType==1):
                print('Answer received')
                break

    device.close()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
