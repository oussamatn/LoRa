#!/usr/bin/python
# -*- coding: UTF-8 -*- 


import paho.mqtt.publish as publish
import serial
import time
import re
import json
#import packer
import base64

BAUDRATE = 57600               # the baud rate we talk to the microchip RN2483
MAX_PAYLOAD_LENGTH = 121
SERVER_IP = "164.132.49.231"
#
# start here
#

try:
    input = raw_input
except NameError:
    pass

serial_port = "/dev/ttyS0"

# open up the FTDI serial port to get data transmitted to lora
ser = serial.Serial(serial_port, BAUDRATE)

if ser.isOpen() == False:
    ser.open()

# The default settings for the UART interface are
# 57600 bps, 8 bits, no parity, 1 Stop bit, no flow control.
ser.bytesize = 8
ser.parity   = "N"
ser.stopbits = 1
ser.timeout  = 5


print('----------------------------------')

print('cmd> radio cw off')
ser.write(b'radio cw off\r\n')
print(str(ser.readline()))

# -----------------------------

print('cmd> radio set mod lora')
ser.write(b'radio set mod lora\r\n')
print(str(ser.readline()))

# decimal representing the frequency,
# from 433000000 to 434800000 or from 863000000 to 870000000, in Hz.
print('cmd> radio set freq 868100000')
ser.write(b'radio set freq 868100000\r\n')
print(str(ser.readline()))

# signed decimal number representing the transceiver output power,
# from -3 to 15.
print('cmd> radio set pwr 14')
ser.write(b'radio set pwr 14\r\n')
print(str(ser.readline()))

print('cmd> radio set sf sf7')
ser.write(b'radio set sf sf7\r\n')
print(str(ser.readline()))

print('cmd> radio set afcbw 41.7')
ser.write(b'radio set afcbw 41.7\r\n')
print(str(ser.readline()))

print('cmd> radio set rxbw 125')
ser.write(b'radio set rxbw 125\r\n')
print(str(ser.readline()))

print('cmd> radio set prlen 8')
ser.write(b'radio set prlen 8\r\n')
print(str(ser.readline()))

print('cmd> radio set cr 4/5')
ser.write(b'radio set cr 4/5\r\n')
print(str(ser.readline()))

print('cmd> radio set wdt 0')
ser.write(b'radio set wdt 0\r\n')
print(str(ser.readline()))

print('cmd> radio set sync 12')
ser.write(b'radio set sync 12\r\n')
print(str(ser.readline()))

print('cmd> radio set bw 125')
ser.write(b'radio set bw 125\r\n')
print(str(ser.readline()))

# -----------------------------


# pauses the LoRaWAN stack functionality to allow transceiver (radio) configuration
# must be called before any radio transmission or reception
print('cmd> mac pause')
ser.write(b'mac pause\r\n')
print(str(ser.readline()))


print('----------------------------------')

try:
    while True:
        ser.write(b'radio rx 0\r\n')
        ret = ser.readline()

        if ret == "ok" or "radio_tx_ok" :

            payload = ser.readline().decode()

            print(payload)
            
            if len(str(payload)) > 5 and payload != "radio_err":
                #publish.single("sensor", payload, hostname="164.132.49.231")
                payload = str(payload).split("  ", 1)[1]
                print(payload)
                print ("decoding ...")
                payload = payload.replace("\r\n", "")
                payload = base64.b16decode(str(payload)).decode()
                print (payload)
                if "ok " in str(payload):
                    payload = str(payload).replace("ok ", "")
                    print (payload)
                    payload = payload.split(';')
                    for data in payload:
                        data = data.split(',')
                        print(data[0])
                        if data[0] == 't':
                            publish.single("sensor/temperature",data[1] , hostname=SERVER_IP)
                        if data[0] == 'Bvol':
                            publish.single("sensor/Bvol",data[1] , hostname=SERVER_IP)
                        if data[0] == 'Bam':
                            publish.single("sensor/Bam",data[1] , hostname=SERVER_IP)
                        if data[0] == 'Bcyc':
                            publish.single("sensor/Bcyc",data[1] , hostname=SERVER_IP)
                        if data[0] == 'Btemp':
                            publish.single("sensor/Btemp",data[1] , hostname=SERVER_IP)
                        if data[0] == 'soc':
                            publish.single("sensor/soc",data[1] , hostname=SERVER_IP)


            if re.match('radio_rx', str(payload).strip()):
                data = payload
                print(payload)
                print('----------------------------------')

finally:
    ser.close()
