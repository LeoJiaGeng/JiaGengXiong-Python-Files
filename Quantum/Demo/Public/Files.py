'''查找文件夹内所有文件，当前目录，删除，重命名，指定的文件是否在其中
'''
import os

class ReFilenames():
    '''读取指定文件内，包括子文件夹所有的后缀名'''
    def __init__(self, format_end):
        self.__format_end = format_end
        self.file_list = []

    def __str__(self) -> str:
        return self.suffix

    def __len__(self) -> int:
        return len(self.file_list)

    @property
    def suffix(self):
        return self.__format_end

    @suffix.setter
    def suffix(self, name):
        self.__format_end = name
    
    def get_all_files(self, dir, only_name = False, without_suffix = False):
        '''获取文件夹内及其子文件夹中所有带有后缀为self.__format_end的文件'''
        self.file_list = []
        for root_dir, sub_dir, files in os.walk(dir):
            # 对文件列表中的每一个文件夹进行处理
            for file in files:
                # 对每个文件夹中的文件进行处理
                if file.endswith(self.suffix):
                    # 寻找xlsx尾缀的文件
                    if not only_name:
                        file_name = os.path.join(root_dir, file)
                        # 拼接文件名和根目录
                        self.file_list.append(file_name)
                    elif only_name and (not without_suffix):
                        # 直接输出文件名
                        self.file_list.append(file) 
                    else:
                        only_file_name = file.split(".")[0]
                        self.file_list.append(only_file_name)
        if self.file_list == []:
            print("没有匹配到该后缀名的文件")             
        return self.file_list

    def sort_file_names(self):
        self.file_list.sort()

    def filename_and_fileabsroute(self, foldername):
        '''获取文件夹内所有文件的名字和绝对路径'''
        filename_list = self.get_all_files(foldername, True, True)
        fileroute_list = self.get_all_files(foldername)
        return zip(filename_list, fileroute_list)

class SaveFile(object):
    def __init__(self):
        pass

    def save_n(self, filename, dataList):
        with open(filename, mode="+a", encoding="utf-8") as file_obj:
            for data in dataList:
                file_obj.write(str(data)+"\n")
            file_obj.close()

    def save(self, filename, dataList):
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, mode="+a", encoding="utf-8") as file_obj:
            for data in dataList:
                file_obj.write(str(data))
            file_obj.close()

class OpenFile(object):
    def __init__(self):
        pass

    def read_file(self, file_name, location=None, length=-1):
        with open(file_name) as file_obj:
            file_obj.seek(location)
            content = file_obj.read(length)
            return content
        
class CreateFile(object):
    def __init__(self):
        pass

    def creat_file(self, file_name):
        
        pass
    

if __name__ == "__main__":
    A = ReFilenames("log")
    #print(A._read_all_files__format_end)
    print(A)
    #print(A.get_all_files(r"D:\Document\Python_Files\Project"))
    print(len(A))
    B = SaveFile()
    B.save("save.txt",A.get_all_files(r"C:\Users\DELL\Desktop\C4xianan\TFAA\extract data", True, True))
