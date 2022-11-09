import os
import datetime
import pytz
import shutil

class Directory():
    def __init__(self):
        self.cur_dir_path = os.path.dirname(__file__)
        self.data_dir_name = "data"
        self.image_dir_name = "image"
        self.sensor_dir_name = "sensor"
        self.data_dir_path = os.path.join(self.cur_dir_path, self.data_dir_name)
    
    def DirSetting(self, calf_id): # 基本となるディレクトリの作成
        os.makedirs(self.data_dir_path, exist_ok=True)
        
        image_dir_path = os.path.join(self.data_dir_path,calf_id,self.image_dir_name)
        os.makedirs(image_dir_path, exist_ok=True)
        
        sensor_dir_path = os.path.join(self.data_dir_path,calf_id,self.sensor_dir_name)
        os.makedirs(sensor_dir_path, exist_ok=True)
    
    def CreateNumImageDir(self, calf_id): # 新しいディレクトリの作成
        image_dir_path = os.path.join(self.data_dir_path,calf_id,self.image_dir_name)
        self.CreateNumDir(image_dir_path)
    
    def CreateNumSensorDir(self, calf_id): # 新しいディレクトリの作成
        sensor_dir_path = os.path.join(self.data_dir_path,calf_id,self.sensor_dir_name)
        self.CreateNumDir(sensor_dir_path)
    
    def GetLatestNumImageDir(self, calf_id): # 1番新しいディレクトリのpathの取得
        image_dir_path = os.path.join(self.data_dir_path,calf_id,self.image_dir_name)
        try:
            path = self.GetLatestDir(image_dir_path)
        except:
            self.CreateNumImageDir(calf_id)
            path = self.GetLatestDir(image_dir_path)
        return path
    
    def GetLatestNumSensorDir(self, calf_id): # 1番新しいディレクトリのpathの取得
        sensor_dir_path = os.path.join(self.data_dir_path,calf_id,self.sensor_dir_name)
        try:
            path = self.GetLatestDir(sensor_dir_path)
        except:
            self.CreateNumSensorDir(calf_id)
            path = self.GetLatestDir(sensor_dir_path)
        return path
    
    def OrganizeDir(self, path): # zip化と元のディレクトリの削除
        self.CreateZip(path)
        self.DeleteDir(path)
    
    def CreateZip(self, path): # ディレクトリのzip化
        dir_name = os.path.join("..\\",path)
        shutil.make_archive(dir_name, format="zip", root_dir=path)
    
    def DeleteDir(self, path): # ディレクトリを削除
        shutil.rmtree(path)
    
    def GetFilesDir(self, path): # 指定したpath直下にあるフォルダ名のリストの取得
        try:
            files = os.listdir(path)
            files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        except:
            os.makedirs(path, exist_ok=True)
            files = os.listdir(path)
            files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        return files_dir
    
    def CreateNumDir(self, path): # 指定したpathから直下に0から始まるフォルダを作成する
        files_dir = self.GetFilesDir(path)
        num = self.CountDir(path)
        new_dir_path = os.path.join(path, str(num))
        os.makedirs(new_dir_path, exist_ok=True)
    
    def GetLatestDir(self, path): # 指定したpath直下にある最新のフォルダ名の取得
        return os.path.join(path,self.GetFilesDir(path)[-1])
    
    def CountFiles(self, path): # 指定したpath直下にあるファイル数の取得
        files = os.listdir(path)
        files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
        return len(files_file)
    
    def CountDir(self, path): # 指定したpath直下にあるファイルとサブディレクトリ数の取得
        files = os.listdir(path)
        return len(files)
    
    def GetDay(self): # 日付データの取得
        dt = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        DAY  = dt.strftime('%Y%m%d')
        return DAY
    
    def GetSecond(self): # 日付データの取得
        dt = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        SECOND  = dt.strftime('%Y%m%d_%H_%M_%S')
        return SECOND

if __name__ == "__main__":
    # 子牛id
    calf_id = "calf_id_0"
    
    # ディレクトリの用意
    directory = Directory()
    # directory.DirSetting(calf_id)
    
    # 新しいディレクトリの作成
    # directory.CreateNumSensorDir(calf_id)
    # directory.CreateNumImageDir(calf_id)
    
    # zip化のテスト
    import json
    for i in range(20):
        path = directory.GetLatestNumSensorDir(calf_id)
        file_path = os.path.join(path, str(i)+".json")
        with open(file_path,"w") as f:
            data = {'k1': 1, 'k2': 2, 'k3': 3}
            json.dump(data, f, indent=4)
        if directory.CountFiles(path) == 5:
            directory.OrganizeDir(path)
            directory.CreateNumSensorDir(calf_id)
            
