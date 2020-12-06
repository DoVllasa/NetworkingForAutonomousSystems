from xbee import transmit, receive, atcmd
import json
import utime

routing_table_entries = []
route_discovery_table_entries = []

message_to_send = {
                'ty': 4,
                'sa': 0,
                'da': 2,
                'me': 'Hello World',
            }

""""
ty = type
id = identifier
da = destination_address
sa = source_address
ts = timestamp
pc = path_cost
fc = forward_cost
nha = next_hop_address
rc = residual_cost
ri = rreq_process_id
rsa = rreq_send_address
ep = expiration_time
"""


def listen():
    while True:
        msg = receive()

        if msg:
            try:
                packet = json.loads(msg['payload'])
                if packet['ty'] == 2:
                    # Receive RREQ
                    has_set = set_discovery_routing_table_entry(packet, str(msg['sender_nwk']))
                    if has_set:
                        if packet['da'] == get_source_address():
                            # Send RREP
                            send_rrep(get_source_address(), packet['sa'], packet['id'], 0)
                        else:
                            if is_destination_in_routing_table(packet['da']):
                                # Forward RREQ by unicast transmission
                                transmit(get_next_hop_for_destination(packet['da']), json.dumps(packet))
                            else:
                                # Broadcast RREQ
                                transmit(0xFFFF, json.dumps(packet))
                elif packet['ty'] == 3:
                    # Receive RREP
                    set_routing_table(packet, str(msg['sender_nwk']))

                    if packet['da'] == get_source_address():
                        # Confirm route establishment
                        print('Route established')
                        send_message('2', message_to_send)
                        break
                    else:
                        # Fotward RREP towards source
                        send_rrep(packet['sa'], packet['da'], packet['id'], int(packet['pc']) + 1)
                elif packet['ty'] == 4:
                    if str(packet['da']) == str(get_source_address()):
                        print(str(packet['me']))
                    else:
                        transmit(int(get_next_hop_for_destination(packet['da'])), json.dumps(packet))
                        print('Sent to next hop')

            except ValueError as e:
                print(msg['payload'])


def set_routing_table(rrep, sender):
    for index in range(0, len(route_discovery_table_entries) - 1):
        if route_discovery_table_entries[index]['ri'] == rrep['id']:
            if rrep['pc'] < route_discovery_table_entries[index]['rc'] or route_discovery_table_entries[index]['rc'] == 0:

                for index2 in range(0, len(routing_table_entries) - 1):
                    if routing_table_entries[index2]['da'] == rrep['sa']:
                        routing_table_entries.remove(routing_table_entries[index2])

                new_routing_table_entry = {
                    'da': rrep['sa'],
                    'nha': sender,
                    'ts': 10,
                }

                routing_table_entries.append(new_routing_table_entry)


def send_rrep(source, destination, identifier, path_cost):
    for discovery_table in route_discovery_table_entries:
        if discovery_table['ri'] == identifier:
            rrep = {
                'ty': 3,
                'sa': source,
                'da': destination,
                'id': identifier,
                'pc': path_cost,
            }

            transmit(int(discovery_table['rsa']), json.dumps(rrep))


def get_next_hop_for_destination(destination):
    for routing_table in routing_table_entries:
        if str(destination) == str(routing_table['da']):
            return routing_table['nha']


def is_destination_in_routing_table(destination):
    for routing_table in routing_table_entries:
        if destination == routing_table['da']:
            return True
    else:
        return False


def set_discovery_routing_table_entry(entry, sender):
    for index in range(0, len(route_discovery_table_entries) - 1):
        if route_discovery_table_entries[index]['ri'] == entry['id']:
            if route_discovery_table_entries[index]['fc'] > entry['pc']:
                entry_with_lower_cost = transform_rreq_into_routing_discovery(entry, sender)
                route_discovery_table_entries[index] = entry_with_lower_cost
                return True
            break
    else:
        new_entry = transform_rreq_into_routing_discovery(entry, sender)
        route_discovery_table_entries.append(new_entry)
        return True

    return False


def transform_rreq_into_routing_discovery(entry, sender):
    rreq_process_id = entry['id']
    forward_cost = entry['pc']
    residual_cost = 0
    expiration_time = 10

    new_entry = {
        'ri': rreq_process_id,
        'rsa': sender,
        'fc': forward_cost,
        'rc': residual_cost,
        'et': expiration_time
    }
    return new_entry


def init_route_discovery(destination):
    rreq = {
        'ty': 2,
        'sa': get_source_address(),
        'da': destination,
        'id': get_source_address() + destination,
        'pc': 0
    }

    transmit(0xFFFF, json.dumps(rreq))
    listen()


def send_message(destination, message):
    for table_entry in routing_table_entries:
        if table_entry['da'] == destination:
            transmit(int(table_entry['nha']), json.dumps(message))
            print('Sent to next hop')
            break
    else:
        print('initiate route discovery')
        init_route_discovery(destination)


def reset_routing_table_entries():
    routing_table_entries = []


def get_source_address():
    return str(atcmd('MY'))


if '0' == get_source_address():
    send_message('2', message_to_send)
else:
    listen()
