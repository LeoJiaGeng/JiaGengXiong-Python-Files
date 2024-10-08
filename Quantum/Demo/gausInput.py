from Public.Files import ReFilenames, SaveFile
from Public.FindData import FindInfo
from Public.common import *
import os

class GauInput():
    def __init__(self):
        self.cur_folder = os.getcwd()
        pass

    # This function is called by the Gaussian
    def create_gjfs(self, foldername, prefix = "", suffix = "", file_type="Unknow", read_type="GauOutFile"):
        """读取指定文件夹内所有log文件，替换成新模板的输入文件，IRC和柔性SCAN自动屏蔽"""
        if read_type == "GauOutFile":
            name_obj = ReFilenames("log")
        elif read_type == "GauInFile":
            name_obj = ReFilenames("gjf")
        write_file = SaveFile()

        # 设置文件的前后缀，默认gif文件
        if prefix != "":
            prefix = prefix + "-"
        if suffix != "":
            suffix = "-" + suffix

        # 未传参则以读取文件为准，传参优先级最高！
        type_flag = False
        if file_type == "Unknow":
            type_flag = True

        for name, fileabsroute in name_obj.filename_and_fileabsroute(foldername):
            file_type == "Unknow"
            if read_type == "GauOutFile":
                read_file = self.read_from_outfile(fileabsroute)
            elif read_type == "GauInFile":
                read_file = self.read_from_inputfile(fileabsroute)
            else:
                print("Err! Unknow file type")

            # 判断文件如果读取失败，则不生成文件！有输出提醒
            if len(read_file) == 1:
                print("Err! Nothing to read")
                continue 
            # 未传参则以读取文件为准，传参优先级最高！
            if type_flag:
                file_type = read_file[-1][0]

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
            elif file_type == "HIGH-SP":
                write_file.save(new_file_name, self.replace_contents(chk_name,read_file,"HIGH-SP"))
            elif file_type == "INPUT":
                write_file.save(new_file_name, self.replace_contents(chk_name,read_file,"INPUT"))
            elif file_type == "F-OPT":
                write_file.save(new_file_name, self.replace_contents(chk_name,read_file,"F-OPT"))
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
        elif type == "HIGH-SP":
            file_template = os.path.join(self.cur_folder, "Template/HIGH-SP-template.txt")
        elif type == "INPUT":
            file_template = os.path.join(self.cur_folder, "Template/INPUT-template.txt")
        elif type == "F-OPT":
            file_template = os.path.join(self.cur_folder, "Template/F-OPT-template.txt")
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

    # 从单个gjf文件中读取信息，返回坐标、电荷和自旋多重度，方便在view操作后批量更改
    def read_from_inputfile(self, filename, only_corrds=True):
        ret_list = []
        write_flag = False
        # 只允许进入一次读取坐标
        flag_times = 0
        with open(filename) as file_obj:
            for line in file_obj.readlines():
                # 仅读取坐标，坐标空行后的信息丢弃
                if only_corrds:
                    if write_flag == True and line == '\n':
                        write_flag = False
                if write_flag:
                    ret_list.append(line[:-1]) # 去掉末尾的换行符
                    # 通过电荷和自旋多重度的数字特性来判断位置是否开始
                if check_list_all_digit(list(line.strip().split(" "))):
                    if flag_times == 0:
                        write_flag = True
                        charge,multiplicity = list(line.strip().split(" "))
                    flag_times += 1
        ret_list.append(["INPUT", charge, multiplicity])
        return ret_list

if __name__ == '__main__':
    A = GauInput()
    B = A.create_gjfs(r"C:\Users\DELL\Desktop\transfer\test",suffix = "-irc",file_type="IRC")
    # B = A.create_gjfs(r"C:\Users\DELL\Desktop\transfer\test",file_type="IRC")
    # C = A.read_coord_inputfile(r"E:\CF3SO2F\KF_SO2Cl\new\Gas\o-TS1-gas.gjf",True)
    # print (C)
    # D = A.replace_contents("A.gjf",C,"OPT")
    # print (D)
