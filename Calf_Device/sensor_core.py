import sys
import threading
from traceback import print_exc
import adafruit_amg88xx
import board
import VL53L1X
import busio
import time

# load config
from config import DISTANCE_MODE, INTERVAL

class ThermoSensorConn():

    def __init__(
        self,
        address=0x68
    ):
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.amg88 = adafruit_amg88xx.AMG88XX(
            self.i2c_bus, addr=address
        )
        time.sleep(.1)


class ToFSensorConn():

    def __init__(
        self,
        i2c_bus=1,
        address=0x29,
        distance_mode: int = None,
        debug=True,
        inteructive_mode = False,
        DISTANCE_MODE : int = 1,
    ):
        
        self.vl53 = VL53L1X.VL53L1X(i2c_bus=i2c_bus, i2c_address=address)
        self.vl53.open()
        self.DISTANCE_MODE = DISTANCE_MODE
        self.inteructive_mode = inteructive_mode

        if distance_mode is None:
            self.set_distance_mode()
        else:
            self.tof.distance_mode = distance_mode

        self.vl53.start_ranging(distance_mode)
        self.data_ready = True

    def set_distance_mode(self):
        
        if self.inteructive_mode:
            print("Select a distance mode")
            print("1). SHORT mode")
            print("2). MEDIUM mode")
            print("3). LONG mode ")
            selected = input('>> ')

            if not selected.isdigit():
                self.set_distance_mode()
                return

            selected = int(selected)
            
            if selected <= 0 or selected > 3:
                self.set_distance_mode()
                return
            
            self.distance_mode = selected
        else:
            self.distance_mode = str(self.DISTANCE_MODE)
        print(f"distance mode : {self.DISTANCE_MODE}")
    
    def distance(self):
        self.vl53.start_ranging(self.distance_mode)
        distance_mm = self.vl53.get_distance()
        self.vl53.stop_ranging()
        return distance_mm
    
    def distance_list(self, num=5):
        distance_mm_list = []
        self.vl53.start_ranging(self.distance_mode)
        for i in range(num):
            distance_mm = self.vl53.get_distance()
            distance_mm_list.append(distance_mm)
        self.vl53.stop_ranging()
        return distance_mm_list

def lab_room_debug(
    thermo_conn,
    tof_conn,
):
    try:

        amg88 = thermo_conn.amg88
        vl53 = tof_conn.vl53

        while True:
            if tof_conn.data_ready:
                print("#" * 128)
                temperature = amg88.pixels
                distance = vl53.get_distance() * 10

                print("temperature(℃): ")
                for row in temperature:
                    print(["{0:.1f}".format(temp) for temp in row])
                print("distance(mm): ")
                print(f"{distance}")

                print("#" * 128)
                time.sleep(1.0)
    except KeyboardInterrupt:
        print("Exit by Keyboard interrupt.")
        raise KeyboardInterrupt
    except:
        print_exc()


if __name__ == "__main__":
    thermo_conn = ThermoSensorConn()
    tof_conn = ToFSensorConn(DISTANCE_MODE=DISTANCE_MODE)
    try:
        lab_room_debug(thermo_conn=thermo_conn, tof_conn=tof_conn)
    except KeyboardInterrupt:
        sys.exit()
