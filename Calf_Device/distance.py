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
    tof_conn: ToFSensorConn,
    server_conn: ServerConn,
    calf_id : str,
    print_debug : bool = True,
    INTERVAL : int = 5,
):

    try:        
        tof_sensor = tof_conn.vl53
        
        # send calf id
        server_conn.SendCalfId(calf_id)
        
        while True:
            cur_data = {}
            start = time.time()
            
            if tof_conn.data_ready:
                # get data
                dt = datetime.datetime.now()
                distance_mm_list = tof_conn.distance_list(num=5)
                cur_data["dt"] = str(dt)
                cur_data["distance_mm_list"] = distance_mm_list
                json_data = json.dumps(cur_data)
                
                # send data
                server_conn.SendSensor(json_data)

            if print_debug:
                print("#" * 128)
                print(f"{cur_data}")
            
            end = time.time()
            execution_time = end - start
            print(f"execution_time : {execution_time}")
            time.sleep(INTERVAL - execution_time)

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
    calf_id = load_setting.GetCalfInfo()["calf_id"]
    connect_info = load_setting.GetConnInfo()
    
    tof = ToFSensorConn()

    server_conn = ServerConn(connect_info=connect_info)
    server_conn.ConnectToServer()
    
    main(tof_conn=tof, server_conn=server_conn, calf_id=calf_id, INTERVAL=2)