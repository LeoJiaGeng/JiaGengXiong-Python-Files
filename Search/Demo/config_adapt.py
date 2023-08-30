import os
from Public.config import Config

class Config_Adapt(Config):
    def __init__(self, file_name):
        super().__init__(file_name)
        if file_name not in os.listdir(os.getcwd()):
            self.create_file()
        
    def create_file(self):
        self.add_section("input")
        self.set_config("input", "file_name", "D:/Document/Python_Files")
        self.set_config("input", "suffix", "py")

if __name__ == "__main__":
    config = Config_Adapt()
    print(config.get_config("input", "suffix"))

                    
