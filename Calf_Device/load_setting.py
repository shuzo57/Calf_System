import json
import os

class LoadSetting():
    def __init__(self, file_name="SETTING.json"):
        self.cur_directory : str = os.path.dirname(__file__)
        self.file_name = os.path.join(self.cur_directory, file_name)
        with open(self.file_name, "r") as f:
            self.data = json.load(f)
    
    def GetAllInfo(self) -> dict:
        return self.data
    
    def GetConnInfo(self) -> dict:
        return self.data["connect"]
    
    def GetImgInfo(self) -> dict:
        return self.data["image"]
    
    def GetCalfInfo(self) -> dict:
        return self.data["calf"]

if __name__ == "__main__":
    load_setting = LoadSetting()
    print(load_setting.GetCalfInfo())
    print(load_setting.GetConnInfo())
    print(load_setting.GetImgInfo())