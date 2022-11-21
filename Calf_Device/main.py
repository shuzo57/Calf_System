import json
import datetime
from traceback import print_exc
from sensor_core import ThermoSensorConn, ToFSensorConn
from server_connection import ServerConn
from PicameraCapture import PicameraConn
import time

# load config
from config import DISTANCE_MODE, INTERVAL

def main(
    amg_conn: ThermoSensorConn,
    tof_conn: ToFSensorConn,
    camera_conn: PicameraConn,
    server_conn: ServerConn,
    calf_id : str,
    print_debug : bool = True,
    INTERVAL : int = 10
):
    try:
        thermo_sensor = amg_conn.amg88
        tof_sensor = tof_conn.vl53
        
        cur_data = {}        
        if tof_conn.data_ready:
            # get data
            dt = datetime.datetime.now()
            dt = dt.strftime("%Y_%m_%d_%H_%M_%S")
            temperature = thermo_sensor.pixels
            distance_mm_list = tof_conn.distance_list(num=5)
            img = camera_conn.capture()
            cur_data["dt"] = dt
            cur_data["temprature"] = temperature
            cur_data["distance_mm_list"] = distance_mm_list
            json_data = json.dumps(cur_data)
            
            # connect to server
            server_conn.ConnectToServer()
            # send calf id
            server_conn.SendCalfId(calf_id)
            # send data
            server_conn.SendSensor(json_data, dt)
            #close soket 
            server_conn.SockClose()
            
            # connect to server
            server_conn.ConnectToServer()
            # send calf id
            server_conn.SendCalfId(calf_id)
            # send data
            server_conn.SendImg(img, dt)
            #close soket 
            server_conn.SockClose()
            
        if print_debug:
            print("#" * 128)
            print(f"{cur_data}")

    except KeyboardInterrupt:
        server_conn.SockClose()
        print("KeyboardInterruput.")
        raise KeyboardInterrupt
    except:
        print_exc()
        print("error in main()")

if __name__ == "__main__":
    from load_setting import LoadSetting
    load_setting = LoadSetting()
    calf_info = load_setting.GetCalfInfo()
    calf_id = calf_info["calf_id"]
    connect_info = load_setting.GetConnInfo()
    
    amg = ThermoSensorConn()
    tof = ToFSensorConn(DISTANCE_MODE=DISTANCE_MODE)
    camera = PicameraConn()

    server_conn = ServerConn(connect_info=connect_info)
    
    main(amg_conn=amg, tof_conn=tof, server_conn=server_conn, camera_conn=camera, calf_id=calf_id)