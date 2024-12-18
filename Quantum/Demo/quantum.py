'''
批量整理log文件的能量，频率和坐标
'''

from Public.Files import ReFilenames
from Public.Excel import Excels
from Public.Word import WordDriver
from Public.decoration import Decorator
from Public.FindData import FindInfo
from Public.common import *

class Quantum(ReFilenames):
    ENERGY = 0
    FREQ = 1
    COORD = 2
    CBS_ONE_ENERGY = 3
    CBS_MULTI_ENERGY = 4
    OTHERS = 5
	
    def __init__(self, type, file_name, standard_data1=0.0, standard_data2=0.0):
        super().__init__(type)
        self.file_name = file_name
        self.full_data = []
        self.files_names = self.get_all_files(file_name)
        self.files_only_names = self.get_all_files(file_name, only_name = True, without_suffix = True)
        self.standard_data1 = float(standard_data1) 
        self.standard_data2 = float(standard_data2)

    def read_file(self, head_data, save_type):
        # 储存框架！！！
        self.full_data = head_data

        for full_name, name in zip(self.files_names, self.files_only_names):
            tranList = []
            tranList = [name] + self.save_content(full_name, save_type)   
            self.full_data.append(tranList)

    def save_frame(self, head_data, new_filename, save_type):

        self.read_file(head_data, save_type)
        # 开始写入数据
        root_write_xls = Excels()
        root_write_docx = WordDriver()
        # 在此处修改，增加判断，乱得很，后续修改
        if head_data[0][0] == "文件名(Hartree)":
            # 放置在words中，这个后续更新一下吧！！！
            # temp_list = []
            # for energy in self.full_data[1:]:
                # cont_1 = "ZPE = " + str(energy[1])
                # cont_2 = "HF = " + str(energy[3])
                # temp_cont = [energy[0], cont_1, cont_2]
                # temp_list.append(temp_cont)
            # root_write_docx.write_table(temp_list, filename = new_filename)
            # return self.full_data[1:]

            gibbs_list = []
            energy_list = []

            for energy in self.full_data:
                gibbs_list.append(energy[4])
                energy_list.append(energy[5])
            gibbs_list = gibbs_list[1:]
            energy_list = energy_list[1:]

            for index in range(len(gibbs_list)):
                append_data1 = round((gibbs_list[index] - self.standard_data1)*627.5095,2)
                append_data2 = round((energy_list[index] - self.standard_data2)*627.5095,2)
                self.full_data[index + 1].append(append_data1)
                self.full_data[index + 1].append(append_data2)

        if head_data[0][0] == "文件名(cm-1)":
            root_write_docx.write_table(self.full_data, filename = new_filename)
            return self.full_data[1:]
        if head_data[0][0] == "文件名(xyz)":
            root_write_docx.write_table(self.full_data, filename = new_filename)
            return self.full_data[1:]
        
        root_write_xls.write_excel_lines(self.full_data, filename = new_filename)
        return self.full_data[1:]

    def save_content(self, name, type):
        """"传入不同的文件名，返回不同的序列"""
        compare_list = []
        if (type == self.ENERGY):
            return FindInfo(name).get_energy()
        elif (type == self.FREQ):
            return FindInfo(name).get_freq() 
        elif (type == self.COORD):
            return FindInfo(name).get_coord()[:-1]
        elif (type == self.CBS_ONE_ENERGY):
            return FindInfo(name).get_cbs_sp_energy()
        elif (type == self.OTHERS):
            return FindInfo(name).get_others()
        elif (type == self.CBS_MULTI_ENERGY):
            compare_list = FindInfo(name).get_rocbs_energy()
            if check_list_all_zero(compare_list):
                return FindInfo(name).get_cbs_energy()
            else:
                return compare_list
        else:
            return False

    @Decorator.exe_time("读取文件频率")
    def save_freq(self, filename = "整理好的量化频率文件.docx"):
        full_data = [[ "文件名(cm-1)","频率"]]
        return self.save_frame(full_data, filename, self.FREQ)

    @Decorator.exe_time("读取文件能量")
    def save_energy(self, filename = "整理好的量化能量文件.xls"):
        full_data = [["文件名(Hartree)","Cor_Zero","Cor_Gibbs","HF","Gibbs","E","Rel_Gibbs","Rel_E"]]
        return self.save_frame(full_data, filename, self.ENERGY)        

    @Decorator.exe_time("读取文件坐标")
    def save_cor(self, filename = "整理好的量化坐标文件.docx"):
        full_data = [["文件名(xyz)", "Coordinates (x, y, z in Å) "]]
        return self.save_frame(full_data, filename, self.COORD)  

    @Decorator.exe_time("读取文件cbs能量")
    def save_cbs_energy(self, filename = "整理好的量化cbs能量文件.xls", cbs_type="ONE_LINK"):
        if cbs_type == "ONE_LINK":
            full_data = [["文件名()","CBS_Energy"]]
            return self.save_frame(full_data, filename, self.CBS_ONE_ENERGY)             
        elif cbs_type == "MULTI_LINKS":
            full_data = [["文件名()","MP4","CCSD(T)","MP2","MP4","HF","Int","OIii","T1","E"]]
            return self.save_frame(full_data, filename, self.CBS_MULTI_ENERGY) 
        else:
            print("cbs_type error")

    @Decorator.exe_time("读取文件其他信息")
    def save_others(self, filename = "整理好的量化其他信息文件.xls"):
        full_data = [["文件名()", "RC_x_GHz", "RC_y_GHz", "RC_z_GHz", "RC_x_cm-1", "RC_y_cm-1", "RC_z_cm-1","MW", "num_freq"]]
        return self.save_frame(full_data, filename, self.OTHERS) 

    @Decorator.exe_time("查找虚频")
    def print_eigenvectors(self):
        return FindInfo(self.file_name).eigenvectors() 

    @Decorator.exe_time("查找YES")
    def print_eigenvectors_YES(self):
        return FindInfo(self.file_name).eigenvectors_YES() 

if __name__ == "__main__":
    nameType = "log"
    file_folder = r"E:\Research\AP\task-1130\二茂铁-AP\FeR2\Rate\R"
    # file_name = r"D:\data\C2F2O\C2F2_1.log"
    A = Quantum(nameType, file_folder)
    # B = Quantum(nameType, file_name)
    # print(B.print_eigenvectors())
    A.save_others()
    # print(A.length)
