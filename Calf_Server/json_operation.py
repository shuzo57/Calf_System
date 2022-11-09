import json
from directory import Directory
import os

class JsonOpe(Directory):
    def __init__(self):
        super().__init__()
        self.JSON = ".json"
    
    def SaveJson(self, calf_id, json_data):
        TIME  = self.GetSecond()
        data_name = TIME + self.JSON
        dir_path = self.GetLatestNumSensorDir(calf_id)
        data_path = os.path.join(dir_path, data_name)
        
        with open(data_path, 'w') as f:
            json.dump(json.loads(json_data), f, indent=4)
        
        if self.CountFiles(dir_path) == 100: # zip化する条件
            self.OrganizeDir(dir_path)
            self.CreateNumSensorDir(calf_id)

if __name__ == '__main__':
    from load_setting import LoadSetting
    load_setting = LoadSetting()
    
    calf_id : str = "calf_id_0"
    data = json.dumps(load_setting.GetAllInfo()) # 文字列である必要がある
    json_operation = JsonOpe()
    json_operation.SaveJson(calf_id, data)