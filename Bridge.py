import serial

PORT = "COM10"   # change this
BAUD = 9600

esp = serial.Serial(PORT, BAUD, timeout=1)

print("NodeMCU connected through USB")

while True:
    line = esp.readline().decode(errors="ignore").strip()

    if line:
        print(line)
