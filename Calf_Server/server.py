import socket
import threading
import time
from traceback import print_exc
from image_stream import ImageStream
from json_operation import JsonOpe
import sys
from typing import Union

class RaspberryPiConnection():
    def __init__(self, connect_info : dict):
        self.image_stream = ImageStream()
        self.json_opration = JsonOpe()
        self.server_ip = connect_info["server_ip"]
        self.server_port = connect_info["server_port"]
        self.MAX_CONNECTIONS = connect_info["MAX_CONNECTIONS"]
        self.charactor_code = connect_info["charactor_code"]
        self.timeout = connect_info["timeout"]
        self.bufsize = connect_info["bufsize"]
        self.EOT = connect_info["EOT"]
        self.ACK = connect_info["ACK"]
        self.IMG_COMAND = connect_info["IMG_COMAND"]
        self.SENSOR_COMAND = connect_info["SENSOR_COMAND"]
        
        self.new_sock = [None] * self.MAX_CONNECTIONS
        self.receive_th = [None] * self.MAX_CONNECTIONS
        
        self.SetSock()
    
    def SetSock(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.server_ip, self.server_port))
            self.sock.listen(self.MAX_CONNECTIONS)
            print(f"Socket ({self.server_ip}, {self.server_port}) is set.")
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print_exc()
            print("error preparing socket.")
    
    def ConnectToPi(self) -> socket.socket:
        try:
            conn, address = self.sock.accept()
            print(f"Connect to {address}.")
            return conn
        except OSError:
            raise KeyboardInterrupt
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print_exc()
            print("Error in connect_to_pi func.")
    
    def Run(self):
        while True:
            try:
                self.new_sock = self.ConnectToPi()
                self.receive_th = threading.Thread(target=self.Receive, args=(self.new_sock, ))
                self.receive_th.setDaemon(True)
                self.receive_th.start()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except ConnectionResetError:
                raise
            except:
                print_exc()
    
    def Receive(self, sock : socket.socket):
        try:
            # Identify calf_id
            # time out setting
            timeout_flag = False
            start_time = time.time()
            while True:
                calf_id = sock.recv(self.bufsize).decode(self.charactor_code)
                if calf_id:
                    # ACKnowledgement
                    sock.send(self.ACK.encode(self.charactor_code))
                    break
                # time out checker
                if not timeout_flag:
                    end_time = time.time()
                    if self.timeout < end_time - start_time:
                        timeout_flag = True
                        break
                else:
                    print("break")
                    break
            # Identify Command
            start_time = time.time()
            recv_comand = ''
            while True:
                recv_comand = sock.recv(self.bufsize).decode(self.charactor_code)
                # time out checker
                if not timeout_flag:
                    end_time = time.time()
                    if self.timeout < end_time - start_time:
                        timeout_flag = True
                        break
                else:
                    print("break")
                    break
                if recv_comand:
                    # ACKnowledgement
                    sock.send(self.ACK.encode(self.charactor_code))
                    break
            # receive file name (date)
            start_time = time.time()
            recv_datetime = ''
            while True:
                recv_datetime = sock.recv(self.bufsize).decode(self.charactor_code)
                # time out checker
                if not timeout_flag:
                    end_time = time.time()
                    if self.timeout < end_time - start_time:
                        timeout_flag = True
                        break
                else:
                    print("break")
                    break
                if recv_datetime:
                    # ACKnowledgement
                    sock.send(self.ACK.encode(self.charactor_code))
                    break
            # receive data
            start_time = time.time()
            full_msg = b''
            while True:
                # Receive Message
                msg = sock.recv(self.bufsize)
                # time out checker
                if not timeout_flag:
                    end_time = time.time()
                    if self.timeout < end_time - start_time:
                        timeout_flag = True
                        break
                else:
                    break
                full_msg += msg
                if full_msg[-4:] == self.EOT.encode(self.charactor_code):
                    full_msg = full_msg[:-4]
                    if recv_comand == self.IMG_COMAND:
                        full_msg = self.image_stream.BinToImg(full_msg)
                        self.image_stream.SaveImg(calf_id, recv_datetime, full_msg)
                        print(f"{calf_id} send image")
                    elif recv_comand == self.SENSOR_COMAND:
                        full_msg = full_msg.decode(self.charactor_code)
                        self.json_opration.SaveJson(calf_id, recv_datetime, full_msg)
                        print(f"{calf_id} send sensor data")
                    # ACKnowledgement
                    sock.send(self.ACK.encode(self.charactor_code))
                    break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except ConnectionResetError:
            raise
        except:
            print_exc()
        finally:
            # finished soket connection 
            print(f"{calf_id} socket closed")
            sock.close()

if __name__ == "__main__":
    from load_setting import LoadSetting
    try:
        load_setting = LoadSetting()
        connect_info = load_setting.GetConnInfo()
        raspi_conn = RaspberryPiConnection(connect_info=connect_info)
        raspi_conn.Run()
    except KeyboardInterrupt:
        sys.exit()