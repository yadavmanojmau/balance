
"""
Run this file to test PLC --> PC connection
"""
from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "192.168.0.23"   ### ip address of PC
SERVER_PORT = 502    

### Create an instance of the Modbus Client 

c = ModbusClient()
c.host(SERVER_HOST)
c.port(SERVER_PORT)

print("Attempting to connect to PLC...")
time.sleep(5)

if not c.is_open():
    if not c.open():
        print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
if c.is_open():
    print("Done Connecting to PLC...")
    while(1):
        """
         we are sending a data at byte 15 for testing for data transfere
        """
        c.write_single_register(15,1)   
        print("Prceed for the further process",c.write_single_register(13,1))