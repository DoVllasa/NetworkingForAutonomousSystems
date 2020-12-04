from xbee import transmit, receive, atcmd
import json


# class Packet:
#
#     def __init__(self, objectType, source, destination, identifier):
#         self.objectType = objectType
#         self.source = source
#         self.destination = destination
#         self.identifier = identifier


# while True:
#    msg = receive()
#    if msg:
#        print(json.loads(msg['payload']))
#        break

packet = {
    'objectType': 1,
    'source': 2,
    'destination': 3,
    'identifier': 4,
}

transmit(0xFFFF, json.dumps(packet))
