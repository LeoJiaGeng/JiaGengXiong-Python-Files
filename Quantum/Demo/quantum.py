'''
批量整理log文件的能量，频率和坐标
'''

from Public.Files import ReFilenames
from Public.Excel import Excels
from Public.decoration import Decorator
from Public.FindData import FindInfo
from Public.common import *

class Quantum(ReFilenames):
    ENERGY = 0
    FREQ = 1
    COORD = 2
    CBS_ENERGY = 3
    def __init__(self, type, file_name, standard_data=0.0):
        super().__init__(type)
        self.file_name = file_name
        self.files_names = self.get_all_files(file_name)
        self.files_only_names = self.get_all_files(file_name, only_name = True, without_suffix = True)
        self.standard_data = float(standard_data) 

    def save_frame(self, head_data, new_filename, save_type):
        # 储存框架！！！
        full_data = head_data

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

            for index in range(len(gibbs_list)):
                append_data = round((gibbs_list[index] - self.standard_data)*627.5095,2)
                full_data[index + 1].append(append_data)

        root_write.write_excel_lines(full_data, filename = new_filename)
        return full_data[1:]

    def save_content(self, name, type):
        """"传入不同的文件名，返回不同的序列"""
        compare_list = []
        if (type == self.ENERGY):
            return FindInfo(name).get_energy()
        elif (type == self.FREQ):
            return FindInfo(name).get_freq() 
        elif (type == self.COORD):
            return FindInfo(name).get_coord()
        elif (type == self.CBS_ENERGY):
            compare_list = FindInfo(name).get_rocbs_energy()
            if check_list_all_zero(compare_list):
                return FindInfo(name).get_cbs_energy()
            else:
                return compare_list
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

    @Decorator.exe_time("读取文件cbs能量")
    def save_cbs_energy(self, filename = "整理好的量化cbs能量文件.xls"):
        full_data = [["文件名()","MP4","CCSD(T)","MP2","MP4","HF","Int","OIii","E"]]
        return self.save_frame(full_data, filename, self.CBS_ENERGY)  

    @Decorator.exe_time("查找虚频")
    def print_eigenvectors(self):
        return FindInfo(self.file_name).eigenvectors() 

    @Decorator.exe_time("查找YES")
    def print_eigenvectors_YES(self):
        return FindInfo(self.file_name).eigenvectors_YES() 

if __name__ == "__main__":
    nameType = "log"
    file_folder = r"E:\Organized Files\2022_10_10\all_data\TFAA\DL-CBS"
    # file_name = r"D:\data\C2F2O\C2F2_1.log"
    A = Quantum(nameType, file_folder)
    # B = Quantum(nameType, file_name)
    # print(B.print_eigenvectors())
    A.save_cbs_energy()
    # print(A.length)