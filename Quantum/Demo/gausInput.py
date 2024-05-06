from Public.Files import ReFilenames, SaveFile
from Public.FindData import FindInfo
from Public.common import *
import os

class GauInput():
    def __init__(self):
        self.cur_folder = os.getcwd()
        pass

    # This function is called by the Gaussian
    def create_gjfs(self, foldername, prefix = "", suffix = "-gas", file_type="Unknow"):
        """读取指定文件夹内所有log文件，替换成新模板的输入文件，IRC和柔性SCAN自动屏蔽"""
        name_obj = ReFilenames("log")
        write_file = SaveFile()

        # 未传参则以读取文件为准，传参优先级最高！
        type_flag = False
        if file_type == "Unknow":
            type_flag = True

        for name, fileabsroute in name_obj.filename_and_fileabsroute(foldername):
            file_type == "Unknow"
            read_file = self.read_from_outfile(fileabsroute)

            # 判断文件如果读取失败，则不生成文件！有输出提醒
            if len(read_file) == 1:
                print("Err! Nothing to read")
                continue 
            # 未传参则以读取文件为准，传参优先级最高！
            if type_flag:
                file_type = read_file[-1][0]

            # 设置文件的前后缀，默认gif文件
            chk_name = prefix + name + suffix 
            new_file_name = chk_name + ".gjf"

            # 判断文件类型，进行写入
            if file_type == "OPT":
                write_file.save(new_file_name, self.replace_contents(chk_name,read_file,"OPT"))
            elif file_type == "TS":
                write_file.save(new_file_name, self.replace_contents(chk_name,read_file,"TS"))
            elif file_type == "IRC":
                write_file.save(new_file_name, self.replace_contents(chk_name,read_file,"IRC"))
            elif file_type == "IRC-SPLIT":
                chk_name_f = chk_name + "-f" 
                new_file_name_f = chk_name_f + ".gjf"
                write_file.save(new_file_name_f, self.replace_contents(chk_name_f,read_file,"IRC-F"))
                chk_name_r = chk_name + "-r" 
                new_file_name_r = chk_name_r + ".gjf"
                write_file.save(new_file_name_r, self.replace_contents(chk_name_r,read_file,"IRC-R"))
            else:
                print("Err! Unknow file type")

    # 获取模板，替换模板中的数据，返回完整数据
    def replace_contents(self, chk_name, new_content, type=None):
        file_list = []

        # 选择合适的文件模版
        if type == "IRC":
            file_template = os.path.join(self.cur_folder, "Template/IRC-template.txt")
        elif type == "IRC-F":
            file_template = os.path.join(self.cur_folder, "Template/IRC-F-template.txt")
        elif type == "IRC-R":
            file_template = os.path.join(self.cur_folder, "Template/IRC-R-template.txt")
        elif type == "TS":
            file_template = os.path.join(self.cur_folder, "Template/TS-template.txt")
        elif type == "OPT":
            file_template = os.path.join(self.cur_folder, "Template/OPT-template.txt")
        else:
            print("err! unknow file type")
            return []
        
        # 打开文件，替换相应部分返回替换内容
        with open(file_template, mode="r", encoding="utf-8") as file_obj:
            for line in file_obj.readlines():
                if "replace-name" in line:
                    line = line.replace("replace-name", chk_name)
                if "replace-coordinate" in line:
                    line = "\n".join(new_content[:-1])
                if "replace-charge" in line:
                    line = line.replace("replace-charge", new_content[-1][1])
                if "replace-multiplicity" in line:
                    line = line.replace("replace-multiplicity", new_content[-1][2])
                file_list.append(line)
                # print(line[:-1])

        # write_file = SaveFile()
        # write_file.save(new_name,file_list)
        return file_list
    
    # 从单个log文件中读取信息
    def read_from_outfile(self, filename):
        ret_list = []
        # 读取单个文件中的坐标、电荷和自旋多重度
        read_file = FindInfo(filename).get_coord()
        for i in read_file[:-1]:
            # 将逗号置换为空格
            ret_list.append(i.replace(",", " "))
        ret_list.append(read_file[-1])
        return ret_list

    # 从单个gjf文件中读取信息，用途不确定，有点忘记了，后续增加读取电荷和自选多重
    def read_from_inputfile(self, filename, only_corrds=False):
        coordinate_list = []
        write_flag = False
        with open(filename) as file_obj:
            for line in file_obj.readlines():
                # 仅读取坐标，坐标空行后的信息丢弃
                if only_corrds:
                    if write_flag == True and line == '\n':
                        write_flag = False
                if write_flag:
                    coordinate_list.append(line[:-1])
                if check_list_all_digit(list(line.strip().split(" "))):
                    write_flag = True
        return coordinate_list

if __name__ == '__main__':
    A = GauInput()
    B = A.create_gjfs(r"E:\CF3SO2F\KF_SO2Cl\new\Gas",file_type="Unknow")
    # C = A.read_coord_inputfile(r"E:\CF3SO2F\KF_SO2Cl\new\Gas\o-TS1-gas.gjf",True)
    # print (C)
    # D = A.replace_contents("A.gjf",C,"OPT")
    # print (D)
