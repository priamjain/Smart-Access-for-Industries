
import serial
from time import sleep
ser =serial.Serial('/dev/ttyACM0',9600)

while(True):
	print(ser.readline().decode('utf-8'))
