import picamera
import time
from datetime import datetime
import io
import numpy as np
import cv2
from load_setting import LoadSetting

class PicameraConn():
    def __init__(self,) -> None:
        self.camera = picamera.PiCamera()
        self.load_setting = LoadSetting()
        self.width = self.load_setting.GetImgInfo()["shape"]["width"]
        self.height = self.load_setting.GetImgInfo()["shape"]["height"]
        self.color_num = self.load_setting.GetImgInfo()["color_num"]
        self.camera.resolution = (self.width, self.height)
        self.img = np.empty((self.height, self.width, self.color_num), dtype=np.uint8)
        time.sleep(1)
    
    def capture(self) -> np.ndarray:
        self.camera.capture(self.img, format='bgr')
        return self.img
    
    def __del__(self) -> None:
        self.close_picamera()
    
    def start_picamera_preview(self) -> None:
        self.camera.start_preview()

    
    def close_picamera(self) -> None:
        self.camera.stop_preview()
        self.camera.close()

if __name__ == "__main__":
    try:
        PicameraConn = PicameraConn()
        img = PicameraConn.capture()
        print(img)
    except KeyboardInterrupt:
        # PicameraConn = PicameraConn.close_picamera()
        sys.exit()