import cv2
import numpy as np
from typing import Union
import os
from directory import Directory
from load_setting import LoadSetting

class ImageStream(Directory):
    def __init__(self):
        super().__init__()
        self.load_setting = LoadSetting()
        self.width = self.load_setting.GetImgInfo()["shape"]["width"]
        self.height = self.load_setting.GetImgInfo()["shape"]["height"]
        self.color_num = self.load_setting.GetImgInfo()["color_num"]
        self.img_type = self.load_setting.GetImgInfo()["img_type"]
        self.img_shape = (self.height, self.width, self.color_num)
    
    def SaveImg(self, calf_id, img:Union[np.ndarray, bytes]):
        if type(img) is bytes:
            img = self.BinToImg(img)
        
        TIME = self.GetSecond()
        img_name = TIME + self.img_type
        dir_path = self.GetLatestNumImageDir(calf_id)
        img_path = str = os.path.join(dir_path, img_name)
        
        cv2.imwrite(img_path, img)
        
        if self.CountFiles(dir_path) == 10: # zip化する条件
            self.OrganizeDir(dir_path)
            self.CreateNumImageDir(calf_id)

    def ImgToBin(self, img:np.ndarray) -> bytes:
        img_bin = img.tobytes()
        return img_bin
    
    def BinToImg(self, img_bin:bytes) -> np.ndarray:
        img = np.frombuffer(img_bin, dtype=np.uint8).reshape(self.img_shape) # for raspberry pi
        return img
    
    def RgbToGbr(self, img :np.ndarray) -> np.ndarray:
        return img[..., ::-1]
    
    def open(self, img_path) -> np.ndarray:
        img = cv2.imread(img_path)
        return img

if __name__ == '__main__':
    img_path : str = "1.png"
    calf_id : str = "calf_id_0"
    
    image_stream = ImageStream()
    img = image_stream.open(img_path)
    
    image_stream.SaveImg(img, calf_id)