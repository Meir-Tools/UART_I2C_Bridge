import serial
import time

def read_compass():
    uart_port = "COM9"
    baud_rate = 115200

    ser = serial.Serial(uart_port, baud_rate, timeout=2)  # זמן המתנה קריאה ארוך יותר
    time.sleep(2)  # לחכות שהפורט יתייצב

    # פקודה בדיוק כמו שאתה שולח ידנית (תשנה לפי הצורך)
    command = "R:0D:00:20\r\n"
    ser.write(command.encode('utf-8'))

    # קבלת תגובה בשורה שלמה
    response = ser.readline()
    
    ser.close()

    print("Response as bytes:", response)
    print("Response as string:", response.decode(errors='ignore').strip())

    return response

if __name__ == "__main__":
    read_compass()
