import sys
import threading
from traceback import print_exc
import adafruit_amg88xx
import adafruit_vl53l1x
import board
import busio
import time

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
        address=0x29,
        distance_mode: int = None,
        debug=True,
        inteructive_mode = False,
        DISTANCE_MODE: int = 1,
    ):
        self.i2c = board.I2C()
        self.vl53 = adafruit_vl53l1x.VL53L1X(self.i2c)
        self.DISTANCE_MODE = DISTANCE_MODE
        self.inteructive_mode = inteructive_mode

        if distance_mode is None:
            self.set_distance_mode()
        else:
            self.tof.distance_mode = distance_mode

        self.vl53.timing_budget = 100
        if debug:
            self.print_model_info()

        self.vl53.start_ranging()

    def set_distance_mode(
        self
    ):
        if self.inteructive_mode:
            print("Select a distance mode")
            print("1). SHORT mode")
            print("2). LONG mode ")
            selected = input('>> ')

            if not selected.isdigit():
                self.set_distance_mode()
                return

            selected = int(selected)

            if selected <= 0 or selected > 2:
                self.set_distance_mode()
                return

            self.vl53.distance_mode = selected
        else:
            self.distance_mode = str(self.DISTANCE_MODE)
            print(f"distance mode : {self.DISTANCE_MODE}")

    def print_model_info(
        self
    ):
        print("--" * 15)
        model_id, module_type, mask_rev = self.vl53.model_info
        print("Model ID: 0x{:0X}".format(model_id))
        print("Module Type: 0x{:0X}".format(module_type))
        print("Mask Revision: 0x{:0X}".format(mask_rev))
        print("Distance Mode: ", end="")
        if self.vl53.distance_mode == 1:
            print("SHORT")
        elif self.vl53.distance_mode == 2:
            print("LONG")
        else:
            print("UNKNOWN")
        print(f"Timing Budget:{self.vl53.timing_budget}")
        print("--" * 15)


def lab_room_debug(
    thermo_conn,
    tof_conn,
):
    try:

        amg88 = thermo_conn.amg88
        vl53 = tof_conn.vl53

        while True:
            if vl53.data_ready:
                print("#" * 128)
                temperature = amg88.pixels
                distance = vl53.distance * 10

                print("temperature(℃): ")
                for row in temperature:
                    print(["{0:.1f}".format(temp) for temp in row])
                print("distance(mm): ")
                print(f"{distance}")

                vl53.clear_interrupt()
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