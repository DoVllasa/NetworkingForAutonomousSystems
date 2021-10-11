from xbee import transmit, receive, atcmd
import json
import utime

save_identifier = {}

millis = utime.ticks_ms()

while True:
    current_millis = utime.ticks_ms()

    if current_millis - millis >= 30000:
        print('Reset save identifier')
        millis = current_millis
        save_identifier = {}

    msg = receive()
    if msg:
        packet = json.loads(msg['payload'])
        objectType = packet['objectType']
        destination = packet['destination']
        source = packet['source']
        identifier = packet['identifier']
        source_address_self = ''.join('{:02x}'.format(x).upper() for x in atcmd("BL"))
        if destination in source_address_self:
            if identifier not in save_identifier:
                ack_packet = {
                    'objectType': 1,
                    'source': source_address_self,
                    'destination': source,
                    'identifier': identifier,
                }
                transmit(0xFFFF, json.dumps(ack_packet))
                save_identifier[identifier] = ack_packet['objectType']
        else:
            if packet['identifier'] not in save_identifier or save_identifier[identifier] != objectType:
                save_identifier[identifier] = objectType
                transmit(0xFFFF, json.dumps(packet))
