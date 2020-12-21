# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from digi.xbee.devices import XBeeDevice
import json

device = XBeeDevice('/dev/tty.usbserial-AC00J775', 9600)

RED_EP = 0xE8
GREEN_EP = 0xE9
BLUE_EP = 0xEA
USERLED_EP = 0xEB
REMOTE_NODE_ID = "Arduino"

ON_OFF_CLUSTER = 0x0006
LEVEL_CONTROL_CLUSTER = 0x0008

remote_device = None

def main():
    device.open()

    xbee_network = device.get_network()
    global remote_device
    remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
    if remote_device is None:
        print("Could not find the remote local_xbee")
        exit(1)

    #while True:
    controller1()
        #time.sleep(5)

    #device.close()


def pressUserButton():
    command_frame = {
        'commandIdentifier': '0x02',
    }

    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=RED_EP, dest_endpoint=BLUE_EP, cluster_id=ON_OFF_CLUSTER, profile_id=0xC05E)


def controller1():
    #Move to level
    command_frame = {
        'commandIdentifier': '0x04',
        'payload': {
            'level': 0xFE,
            'transitionTime': 3
        }
    }

    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=RED_EP, dest_endpoint=RED_EP,
                           cluster_id=LEVEL_CONTROL_CLUSTER, profile_id=0xC05E)

def controller2():
    #Move
    UP = 0x00
    DOWN = 0x01

    command_frame = {
        'commandIdentifier': '0x05',
        'payload': {
            'moveMode': UP,
            'rate': 5
        }
    }

    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=RED_EP, dest_endpoint=RED_EP,
                           cluster_id=LEVEL_CONTROL_CLUSTER, profile_id=0xC05E)
    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=BLUE_EP, dest_endpoint=BLUE_EP,
                           cluster_id=LEVEL_CONTROL_CLUSTER, profile_id=0xC05E)

def controller3():
    #Step
    UP = 0x00
    DOWN = 0x01

    command_frame = {
        'commandIdentifier': '0x06',
        'payload': {
            'stepMode': DOWN,
            'stepSize': 0x7E,
            'transitionTime': 2
        }
    }

    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=RED_EP, dest_endpoint=RED_EP,
                           cluster_id=LEVEL_CONTROL_CLUSTER, profile_id=0xC05E)
    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=BLUE_EP, dest_endpoint=BLUE_EP,
                           cluster_id=LEVEL_CONTROL_CLUSTER, profile_id=0xC05E)
    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=GREEN_EP, dest_endpoint=GREEN_EP,
                           cluster_id=LEVEL_CONTROL_CLUSTER, profile_id=0xC05E)


def stop():
    command_frame = {
        'commandIdentifier': '0x03'
    }

    device._send_expl_data(remote_device, json.dumps(command_frame), src_endpoint=RED_EP, dest_endpoint=RED_EP,
                           cluster_id=LEVEL_CONTROL_CLUSTER, profile_id=0xC05E)



if __name__ == '__main__':
    main()
