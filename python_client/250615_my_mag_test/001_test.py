import serial
import time

def read_compass():
    # הגדרת פורט UART - תתאים לפי החיבור שלך
    uart_port = "COM9"  # בווינדוס זה יכול להיות "COM3" או דומה
    baud_rate = 115200          # בדוק את קצב העברת הנתונים של המודול
    
    # פתיחת פורט סידורי
    ser = serial.Serial(uart_port, baud_rate, timeout=1)
    
    # המתן קצת שהפורט יפתח ויציב
    time.sleep(2)
    
    # הפקודה לשליחה (במחרוזת)
    command = "R:0x0D:0x00:32\n"  # נניח שהמודול מקבל פקודות בשורת טקסט
    
    # שליחת הפקודה (צריך לשלוח כמחרוזת בייטים)
    ser.write(command.encode('utf-8'))
    
    # המתנה לקבלת תגובה
    time.sleep(0.1)
    
    # קריאת התגובה
    response = ser.read(64)  # נקרא עד 64 בתים (לפי מה שהמודול מחזיר)
    
    # סגירת הפורט
    ser.close()
    
    # הדפסת הנתונים שקיבלנו (בייטים)
    print("Response bytes:", response)
    
    # במידה וצריך לפרש את התשובה - תוסיף כאן לפי הפורמט של המודול שלך
    
    return response

if __name__ == "__main__":
    read_compass()
