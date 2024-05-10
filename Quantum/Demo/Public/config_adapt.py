import os
from Public.config import Config

class Config_Adapt(Config):
    def __init__(self, file_name):
        super().__init__(file_name)
        if file_name not in os.listdir(os.getcwd()):
            self.create_file()
        
    def create_file(self):
        self.add_section("save")
        self.set_config("save", "save_folder", "D:/Document/Python_Files")
        self.set_config("save", "save_file_name", "能量")
        self.set_config("save", "standard_Gdata", "0.0")
        self.set_config("save", "standard_Edata", "0.0")
        self.add_section("search")
        self.set_config("search", "search_file_name", "D:/Document/Python_Files/ts1.log")
        self.add_section("transfer")
        self.set_config("transfer", "trans_update_folder", "D:/Document/Python_Files")
        self.set_config("transfer", "trans_file_name", "D:/Document/Python_Files/ts1.log")
        self.set_config("transfer", "trans_folder_name", "D:/Document")
        self.set_config("transfer", "trans_ruler", "name1 2, name2 3")

if __name__ == "__main__":
    config = Config_Adapt("config.ini")
    print(config.get_config("input", "suffix"))

                    
