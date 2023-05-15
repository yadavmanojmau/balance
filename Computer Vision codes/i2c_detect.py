from smbus2 import SMBus
import time

import smbus2

while True:
    with SMBus(1) as bus:  

        data = [0,120,1,150,0,107]
        print(data)
        bus.write_i2c_block_data(20,0,data)
        time.sleep(5)
        
        data = [0,120,1,150,0,70]
        print(data)
        bus.write_i2c_block_data(20,0,data)
        time.sleep(5)




        
