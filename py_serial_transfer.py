import serial
import time
import string
import random

target_dongle_mac_address = (
    "[0]40:48:FD:E5:2D:AF"  # Change this to the 1st peripheral's mac address.
)
target_dongle_mac_address2 = (
    "[0]40:48:FD:E5:2D:B5"  # Change this to the 2nd peripheral's mac address.
)
your_com_port = "COM7"  # Change this to the com port your dongle is connected to.

connecting_to_dongle = True
trying_to_connect = False
trying_to_connect2 = False

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

print("Connecting to dongle...")
# Trying to connect to dongle until connected. Make sure the port and baudrate is the same as your dongle.
# You can check in the device manager to see what port then right-click and choose properties then the Port Settings
# tab to see the other settings
while connecting_to_dongle:
    try:
        console = serial.Serial(
            port=your_com_port,
            baudrate=57600,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=0,
        )
        if console.is_open.__bool__():
            connecting_to_dongle = False
    except:
        print("Dongle not connected. Please reconnect Dongle.")
        time.sleep(5)

print("Connected to Dongle.")

connected = "0"
connected2 = "0"
while 1 and console.is_open.__bool__():
    console.write(str.encode("AT+DUAL"))
    console.write("\r".encode())
    time.sleep(0.1)
    print("Putting dongle in Dual role and trying to connect to other dongle.")
    while connected == "0":
        time.sleep(0.5)
        if not trying_to_connect:
            console.write(str.encode("AT+GAPCONNECT="))
            console.write(str.encode(target_dongle_mac_address))
            console.write("\r".encode())
            trying_to_connect = True
        dongle_output2 = console.read(console.in_waiting)
        time.sleep(2)
        print("Trying to connect to Peripheral 1...")
        if not dongle_output2.isspace():
            if dongle_output2.decode().__contains__("\r\nCONNECTED."):
                connected = "1"
                print("Connected to 1st device!")                
                time.sleep(5)
            if dongle_output2.decode().__contains__("\r\nDISCONNECTED."):
                connected = "0"
                print("Disconnected!")
                trying_to_connect = False
            dongle_output2 = " "
    while connected2 == "0":
        time.sleep(0.5)
        if not trying_to_connect2:
            console.write(str.encode("AT+GAPCONNECT="))
            console.write(str.encode(target_dongle_mac_address2))
            console.write("\r".encode())
            trying_to_connect2 = True
        dongle_output2 = console.read(console.in_waiting)
        time.sleep(2)
        print("Trying to connect to Peripheral 2...")
        if not dongle_output2.isspace():
            if dongle_output2.decode().__contains__("\r\nCONNECTED."):
                connected2 = "1"
                print("Connected to 2nd device!")                
                time.sleep(5)
            if dongle_output2.decode().__contains__("\r\nDISCONNECTED."):
                connected2 = "0"
                print("Disconnected!")
                trying_to_connect2 = False
            dongle_output2 = " "
    while connected == "1" and connected2 =="1":        
        dongle_output3 = console.read(console.in_waiting)
        delay=10
        close_time=time.time()+delay
        i=0
        while True:
            myConIndex =  ('0000' if i%2 == 0 else '0001')
            console.write(str.encode("AT+TARGETCONN="))
            console.write(str.encode(myConIndex))
            console.write("\r".encode())
            console.write(str.encode("AT+SPSSEND="))
            console.write(str.encode(id_generator()+'-'+myConIndex))
            console.write("\r".encode())
            time.sleep(0.2)
            i+=1
            if time.time()>close_time:
                break
        console.write(str.encode("AT+SPSSEND=[DONE]\r"))
        time.sleep(0.2)
        print("Sending complete!\r\n")
        print("Exiting script...")
        exit()