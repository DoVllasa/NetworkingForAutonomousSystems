import machine as machine
from xbee import transmit, receive, atcmd
import time
import machine

"""
    User LED Aufgabe 2.2.1, zusammen mit pythonProject
    RECEIVER
"""

# i = 0
# print("start receiving")
# pin = machine.Pin('D4', machine.Pin.OUT)
# while True:
#     msg = receive()
#     if msg:
#         iterations = int(msg['payload'])
#
#         while i < iterations:
#             print('LED ON')
#             pin.off()
#             time.sleep(1)
#             print('LED OFF')
#             pin.on()
#             time.sleep(1)
#             i+=1
#         i = 0


"""
    Range Test 2.2.2, zusammen mit pythonProject
    RECEIVER
"""

i = 0
print("start receiving")
while True:
    msg = receive()
    if msg:
        # sender_address = int(msg['payload'])
        # print('SENMDER', sender_address)
        rssi = atcmd('DB')
        transmit(0, str(rssi))
        print('Payload: ', i, ' ' , 'Distanc in DB: ', rssi)
print("start sending")
