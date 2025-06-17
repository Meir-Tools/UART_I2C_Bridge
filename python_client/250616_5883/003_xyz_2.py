import serial
import time
import struct

uart_port = "COM9"
baud_rate = 115200
ser = serial.Serial(uart_port, baud_rate, timeout=1)
time.sleep(2)

command = "R:0x0D:0x03:6\n"

def to_signed(msb, lsb):
    value = (msb << 8) | lsb
    if value >= 0x8000:
        value -= 0x10000
    return value

i = 0
try:
    while True:
        i += 1
        ser.write(command.encode('utf-8'))
        response = ser.read(6)  # קורא בדיוק 6 בתים
        if len(response) == 6:
            x = to_signed(response[0], response[1])
            y = to_signed(response[4], response[5])
            z = to_signed(response[2], response[3])
            print(f"[{i}] X={x}, Y={y}, Z={z}")
        else:
            print(f"[{i}] קיבלתי תגובה לא תקינה:", response)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nיציאה מהלולאה - הופסק על ידי המשתמש.")
finally:
    ser.close()
