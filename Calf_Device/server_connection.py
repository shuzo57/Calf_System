import socket
from image_stream import ImageStream
from load_setting import LoadSetting
import json
import time
from typing import Union
import numpy as np

class ServerConn():
    def __init__(self, connect_info : dict):
        self.image_stream = ImageStream()
        self.server_ip = connect_info["server_ip"]
        self.server_port = connect_info["server_port"]
        self.charactor_code = connect_info["charactor_code"]
        self.bufsize = connect_info["bufsize"]
        self.EOT = connect_info["EOT"]
        self.ACK = connect_info["ACK"]
        self.IMG_COMAND = connect_info["IMG_COMAND"]
        self.SENSOR_COMAND = connect_info["SENSOR_COMAND"]
    
    def ConnectToServer(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"connect ({self.server_ip}, {self.server_port})")
            self.sock.connect((self.server_ip, self.server_port))
            print("connected.")
        except KeyboardInterrupt:
            print("KeyboardInterrupt.")
            raise KeyboardInterrupt
        except:
            print('connection failed.')
            self.SockClose()
    
    def GetSocket(self):
        return self.sock
    
    def SockClose(self):
        try:
            self.sock.close()
            print("Disconnected.")
        except KeyboardInterrupt:
            self.sock.close()
            print("KeyboardInterrupt.")
            raise KeyboardInterrupt
        except:
            pass
    
    def SendSensor(self, json_data:str, dt:str):
        while True:
            self.SendSensorComand()
            msg = self.sock.recv(self.bufsize).decode(self.charactor_code)
            if msg == self.ACK:
                break
        while True:
            self.SendDateTime(dt)
            msg = self.sock.recv(self.bufsize).decode(self.charactor_code)
            if msg == self.ACK:
                break
        while True:
            self.SendSensorData(json_data)
            msg = self.sock.recv(self.bufsize).decode(self.charactor_code)
            if msg == self.ACK:
                break
    
    def SendImg(self, img:Union[np.ndarray, bytes], dt:str):
        while True:
            self.SendImgComand()
            msg = self.sock.recv(self.bufsize).decode(self.charactor_code)
            if msg == self.ACK:
                break
            
        while True:
            self.SendDateTime(dt)
            msg = self.sock.recv(self.bufsize).decode(self.charactor_code)
            if msg == self.ACK:
                break
        while True:
            self.SendImgData(img)
            msg = self.sock.recv(self.bufsize).decode(self.charactor_code)
            if msg == self.ACK:
                break
    
    def SendSensorData(self, json_data:str):
        remain : str = json_data
        while True:
            send_json_data = remain[:self.bufsize]
            self.sock.send(send_json_data.encode(self.charactor_code))
            remain = remain[self.bufsize:]
            if len(remain) <= 0:
                break
        
        self.sock.send(self.EOT.encode(self.charactor_code))
    
    def SendSensorComand(self):
        self.sock.send(self.SENSOR_COMAND.encode(self.charactor_code))
    
    def SendDateTime(self, dt:str):
        self.sock.send(dt.encode(self.charactor_code))
    
    def SendImgData(self, img:Union[np.ndarray, bytes]):
        if type(img) is np.ndarray:
            img = self.image_stream.ImgToBin(img)
        
        remain = img
        while True:
            send_img = remain[:self.bufsize]
            self.sock.send(send_img)
            remain = remain[self.bufsize:]
            if len(remain) <= 0:
                break
        
        self.sock.send(self.EOT.encode(self.charactor_code))
    
    def SendImgComand(self):
        self.sock.send(self.IMG_COMAND.encode(self.charactor_code))
    
    def SendCalfId(self, calf_id : str):
        while True:
            self.sock.send(calf_id.encode(self.charactor_code))
            msg = self.sock.recv(self.bufsize).decode(self.charactor_code)
            if msg == self.ACK:
                break

if __name__ == "__main__":
    from load_setting import LoadSetting
    load_setting = LoadSetting()
    calf_id = load_setting.GetCalfInfo()["calf_id"]
    connect_info = load_setting.GetConnInfo()
    
    server_conn = ServerConn(connect_info=connect_info)
    server_conn.ConnectToServer()
    server_conn.SockClose()