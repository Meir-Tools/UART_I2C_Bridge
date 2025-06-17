import serial
import time


uart_port = "COM9"
baud_rate = 115200
ser = serial.Serial(uart_port, baud_rate, timeout=1)
time.sleep(2)

						 

command = "R:0x0D:0x00:32\n"
								  
						 

# נשלח את הפקודה כל שנייה למשך 10 פעמים
while True:
    ser.write(command.encode('utf-8'))
    response = ser.readline()
    print(f"Response as bytes:", response)
    time.sleep(1)  # השהיה של שנייה

ser.close()

wait = input("Press Enter to continue.")
