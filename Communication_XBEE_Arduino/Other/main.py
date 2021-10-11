# Default template for XBee MicroPython projects
import json

import xbee as xbee

RED_EP = 0xE8
GREEN_EP = 0xE9
BLUE_EP = 0xEA
USERLED_EP = 0xEB

ON_OFF_CLUSTER = 0x0006
LEVEL_CONTROL_CLUSTER = 0x0008


def pressUserButton():
    command_frame = {
        'commandIdentifier': '0x01',
    }

    xbee.transmit(xbee.ADDR_COORDINATOR, json.dumps(command_frame), dest_ep=RED_EP, cluster=ON_OFF_CLUSTER, profile=0xC05E)
    xbee.transmit(xbee.ADDR_COORDINATOR, json.dumps(command_frame), dest_ep=GREEN_EP, cluster=ON_OFF_CLUSTER, profile=0xC05E)
    xbee.transmit(xbee.ADDR_COORDINATOR, json.dumps(command_frame), dest_ep=BLUE_EP, cluster=ON_OFF_CLUSTER, profile=0xC05E)
    xbee.transmit(xbee.ADDR_COORDINATOR, json.dumps(command_frame), dest_ep=USERLED_EP, cluster=ON_OFF_CLUSTER, profile=0xC05E)

pressUserButton()