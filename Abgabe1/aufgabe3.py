from digi.xbee.devices import XBeeDevice
from digi.xbee.util import utils
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time
import threading

device = XBeeDevice('/dev/tty.usbserial-AK05ZGXZ', 9600)


"""
    Aufgabe 3.1 Range Test
"""
# device.open()
# while True:
#     msg = device.read_data()
#     print('DB: ', utils.bytes_to_int(device.get_parameter("DB")))

"""
    Aufgabe 3.2 USER LED
"""

IO_LINE_OUT = IOLine.DIO4_AD4


def main():
    stop = False
    th = None
    try:
        device.open()
        def io_detection_callback():
            while not stop:
                # Read the digital value from the input line.
                io_value = device.get_dio_value(IO_LINE_OUT)
                print("%s: %s" % (IO_LINE_OUT, io_value))

                # Set the previous value to the output line.
                device.set_dio_value(IO_LINE_OUT, io_value)

                time.sleep(1)

        th = threading.Thread(target=io_detection_callback)
        device.set_io_configuration(IO_LINE_OUT, IOMode.DIGITAL_OUT_LOW)

        time.sleep(1)
        th.start()

        input()

    finally:
        stop = True
        if th is not None and th.is_alive():
            th.join()
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()

device.close()
