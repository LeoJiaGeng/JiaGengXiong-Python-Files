
from Public.config import Config
import os

class Config_Adapt(Config):
    def __init__(self, file_name):
        super().__init__(file_name)
        if file_name not in os.listdir(os.getcwd()):
            self.create_file()
        
    def create_file(self):
        self.add_section("input")
        self.set_config("input", "file_name", "D:\OneDrive\桌面\异构体能量对比")
        self.set_config("input", "num", "1")

if __name__ == "__main__":
    config = Config_Adapt()
    print(config.get_config("input", "suffix"))

                    
