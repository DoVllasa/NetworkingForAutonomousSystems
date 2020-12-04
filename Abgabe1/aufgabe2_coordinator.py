from xbee import transmit, receive, atcmd
import machine
import time

"""
    User LED Aufgabe 2.2.1, zusammen mit pythonProject1
    SENDERS
"""
#
# i = 2
# print('Start sending')
# transmit(0xFFFF, str(i))
# print('Stop sending')


"""
    User LED Aufgabe 2.2.2, zusammen mit pythonProject1
    SENDERS
"""

i = 0
print('Start sending')
payload_device1 = []
payload_device2 = []
timeout = 5
while i < 10:
    transmit(1, str(atcmd('MY')))
    while timeout > 0:
        msg = receive()
        if msg:
            payload_device1.append(int(msg['payload']))
            break
        time.sleep(1)
        timeout-=1
    timeout = 5

    transmit(2, str(atcmd('MY')))
    while timeout > 0:
        msg = receive()
        if msg:
            payload_device2.append(int(msg['payload']))
            break
        time.sleep(1)
        timeout-=1
    timeout = 5
    i += 1

print('RSSI_1 MIN: ', min(payload_device1), 'MAX: ', max(payload_device1), 'MEAN: ', sum(payload_device1)/len(payload_device1), 'SUCCESS: ', len(payload_device1)/10 * 100,'%')
print('RSSI_2 MIN: ', min(payload_device2), 'MAX: ', max(payload_device2), 'MEAN: ', sum(payload_device2)/len(payload_device2), 'SUCCESS: ', len(payload_device2)/10 * 100,'%')

print('Stop sending')



####### Sending ######


# i = 0
# print('Start sending')
# transmit(0xFFFF, 'Hello World')
# time.sleep(5)
# transmit(0, 'Hello Coordinator')
# time.sleep(5)
# transmit(1, 'Hello Device1')
#
# print('Stop sending')


####### Receiving ######
#
# i = 0
# print('Start reveiving')
# while i < 3:
#     msg=receive()
#     if msg:
#         i += 1
#         print(msg)
# print('Stop reveiving')
