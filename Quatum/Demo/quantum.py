'''
批量整理log文件的能量，频率和坐标
'''

from Public.Files import ReFilenames
from Public.Excel import Excels
from Public.decoration import Decorator
from Public.FindData import FindInfo

class Quantum(ReFilenames):
    ENERGY = 0
    FREQ = 1
    COORD = 2
    def __init__(self, type, file_name):
        super().__init__(type)
        self.file_name = file_name
        self.files_names = self.get_all_files(file_name)
        self.files_only_names = self.get_all_files(file_name, True)
        self.length = len(self) # 用于显示进度条的

    def save_frame(self, head_data, new_filename, save_type):
        # 储存框架！！！
        full_data = head_data
        try:
            for full_name, name in zip(self.files_names, self.files_only_names):
                tranList = []
                tranList = [name] + self.save_content(full_name, save_type)   
                full_data.append(tranList)
            # 开始写入数据
            root_write = Excels()
            # 在此处修改，增加判断，乱得很，后续修改
            if head_data[0][0] == "文件名(Hartree)":
                gibbs_list = []

                for gibbs_energy in full_data:
                    gibbs_list.append(gibbs_energy[4])
                gibbs_list = gibbs_list[1:]

                gibbs_min_energy = min(gibbs_list)
                for index in range(len(gibbs_list)):
                    full_data[index + 1].append((gibbs_list[index] - gibbs_min_energy)*627.5095)

            root_write.write_excel_lines(full_data, filename = new_filename)
            return True
        except Exception as e:
            print(e)
            return False

    def save_content(self, name, type):
        """"传入不同的文件名，返回不同的序列"""
        if (type == self.ENERGY):
            return FindInfo(name).get_energy()
        elif (type == self.FREQ):
            return FindInfo(name).get_freq() 
        elif (type == self.COORD):
            return FindInfo(name).get_coord()
        else:
            return False

    @Decorator.exe_time("读取文件频率")
    def save_freq(self, filename = "整理好的量化频率文件.xls"):
        full_data = [[ "文件名(cm-1)","频率"]]
        return self.save_frame(full_data, filename, self.FREQ)

    @Decorator.exe_time("读取文件能量")
    def save_energy(self, filename = "整理好的量化能量文件.xls"):
        full_data = [["文件名(Hartree)","Cor-Zero","Cor-Gibbs","HF","Gibbs","E", "Rel_Gibbs"]]
        return self.save_frame(full_data, filename, self.ENERGY)        

    @Decorator.exe_time("读取文件坐标")
    def save_cor(self, filename = "整理好的量化坐标文件.xls"):
        full_data = [["文件名(xyz)"]]
        return self.save_frame(full_data, filename, self.COORD)  
    
    @Decorator.exe_time("查找虚频")
    def print_eigenvectors(self):
        return FindInfo(self.file_name).eigenvectors() 

    @Decorator.exe_time("查找YES")
    def print_eigenvectors_YES(self):
        return FindInfo(self.file_name).eigenvectors_YES() 

if __name__ == "__main__":
    nameType = "log"
    file_names = r"D:\data\C4F7N\C4\g09\cbs"
    file_name = r"D:\data\C2F2O\C2F2_1.log"
    A = Quantum(nameType, file_names)
    B = Quantum(nameType, file_name)
    print(B.print_eigenvectors())
    A.save_cor()
    print(A.length)
