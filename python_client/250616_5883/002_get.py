import serial
import time


uart_port = "COM9" 
baud_rate = 115200 
ser = serial.Serial(uart_port, baud_rate, timeout=1)
time.sleep(2)

response = ser.readline()

command = "R:0x0D:0x00:32\n"  
ser.write(command.encode('utf-8'))
response = ser.readline()

print("Response as bytes:", response)

ser.close()

wait = input("Press Enter to continue.")