"""
查找log文件文件里面的零点能、吉布斯、HF的能量和虚频以及YES，返回数组!!!
"""
import math

class FindInfo():
    # 字典用于查找能量
    energy_key_word = ["Zero-point correction",
                   "Gibbs Free Energy",
                   "Sum of electronic",
                   "thermal Free Energies",
                   "Sum of energy"
                    ]

    # 列表用于查找频率
    freq_key = ["Frequencies --",
                "Low"
                ]

    # 列表用于查找存在YES
    YES_keys = ["Maximum Force",
                "RMS     Force",
                "Maximum Displacement",
                "RMS     Displacement"
                ]

    # 列表用于查找坐标
    coordinates_key = ["Redundant internal coordinates",
                        "Recover connectivity data from disk"
                        ]
    
    # 列表用于查找cbs能量
    rocbs_key = ["ROMP4(SDQ)",
               "CCSD(T)",
               "E(PMP2)",
               "ROMP4(SDQ)",
               "SCF Done:  E(ROHF)",
               "CBS-Int",
               "OIii",
               "T1 Diagnostic"
               ]

    # 列表用于查找rocbs能量
    cbs_key = ["UMP4(SDQ)",
               "CCSD(T)",
               "EUMP2",
               "UMP4(SDQ)",
               "SCF Done:  E(RHF)",
               "CBS-Int",
               "OIii",
               "T1 Diagnostic"
               ]

    # 列表用于查找其他信息，RC,MW,num_freq
    others_key = ["Rotational constants",
               "Molecular mass",
               "Deg. of freedom"
               ] 

    def __init__(self, filename):
        """传入文件名，可以得到需要条件的数组"""
        self.filename = filename
               
    def zero_cor_energy(self, line):
        """查找零点校正能量 """
        line_detail = (line.split("=")[1]).strip()
        line_detail = line_detail.split(" ")[0]
        return float(line_detail) 

    def gibbs_cor_energy(self, line):
        """查找吉布斯校正能量 """
        line_detail = (line.split("=")[1]).strip()
        return float(line_detail) 

    def gibbs_energy(self, line):
        """查找吉布斯能量 """
        line_detail = (line.split("=")[1]).strip()
        return float(line_detail)

    def energy_check(self, check_list, check_count):
        """检查能量是否不存在，是否出现很多次能量，代表文件异常 """
        if (0.0 in check_list) or (check_count != len(self.energy_key_word)):
            print("数据出现异常！")
            return False
        else:
            return True

    def rota_const(self, line):
        """查找转动常数，这是浮点数"""
        line_data = (line.split(":")[1]).strip()
        line_detail = []
        for i in list(line_data.split(" ")):
            if i != "":
                line_detail.append(float(i))    
        return line_detail

    def MW(self, line):
        """查找分子量 """
        line_data = (line.split(":")[1]).strip() 
        return (line_data.split(" ")[0])

    def num_freq(self, line):
        """查找频率数目 """
        line_data = (line.split("freedom")[1]).strip()
        return line_data

    def get_others(self):
        """查找其他信息，包括分子量，转动常数，频率数目"""
        others_list = [0] * 8
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            for line in file_lines:
                if self.others_key[0] in line:
                    others_list[0],others_list[1],others_list[2] = self.rota_const(line)
                elif self.others_key[1] in line:
                    others_list[6] = self.MW(line)
                elif self.others_key[2] in line:
                    others_list[7] = self.num_freq(line)
        
        # 读取的是GHZ，转换为cm-1，换算量是除以30
        others_list[3] = round((others_list[0]/30.0),6)
        others_list[4] = round((others_list[1]/30.0),6)
        others_list[5] = round((others_list[2]/30.0),6)
        print("文件{}其他数据查找完毕\n".format(self.filename))  
        return others_list      

    def get_energy(self):
        """主程序，返回一个查询完的列表 """
        energy_list = [0] * len(self.energy_key_word)
        energy_check_count = 0
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            for line in file_lines:
                if self.energy_key_word[0] in line:
                    energy_list[0] = self.zero_cor_energy(line)
                    energy_check_count += 1
                elif self.energy_key_word[1] in line:
                    energy_list[1] = self.gibbs_cor_energy(line)
                    energy_check_count += 1
                elif self.energy_key_word[3] in line:
                    energy_list[3] = self.gibbs_energy(line)
                    energy_check_count += 1
        
        energy_list[2] = round((energy_list[3] - energy_list[1]),6)
        energy_check_count += 1
        energy_list[4] = round((energy_list[2] + energy_list[0]),6)
        energy_check_count += 1
        print("文件{}能量查找完毕\n".format(self.filename))
        # 进行文件检查
        # if self.energy_check(energy_list, energy_check_count):
        #     return energy_list
        # else:
        #     return [0] * len(self.energy_key_word)
        return energy_list

    def get_freq(self):
        """查找振动频率"""
        freq_list = []
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            for line in file_lines:
                if self.freq_key[0] in line and self.freq_key[1] not in line:
                    line = line.strip()
                    line = line.split(" ")
                    tran_list = self.str_list_to_2float([item for item in line if len(item.split(".")) == 2])
                    if (float(tran_list[0]) < 0.0):
                        tran_list[0] = str(math.fabs(float(tran_list[0]))) + "i"
                    freq_list.extend(tran_list)
        # 转变成一个数据填入       
        one_str = ",".join(freq_list)
        freq_list.clear()
        freq_list.append(one_str)
        print("文件{}频率查找完毕\n".format(self.filename))
        if freq_list == []:
            print("未找到能量数据")
        return freq_list

    def get_coord(self):
        """查找坐标，最后一个元素是文件类别，电荷和自旋多重度"""
        coordinates = []
        # 遇到恢复词，不写入，直接终止循环
        # 遇到冗余内坐标开始记录
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            start_flag = 0
            type_flag = 0
            count = 0
            for line in file_lines:
                # 防止出现从check文件导入，出现同样关键词干扰，因此大于300
                if count > 300:
                    # 必须要start_flag=1之后，代表写完才可以退出，不然则遍历整个文件结束
                    if self.coordinates_key[1] in line and start_flag == 1:
                        break            
                    if start_flag == 1: 
                        line = line.strip()
                        coordinates.append(line)
                    if self.coordinates_key[0] in line:
                        start_flag = 1
                # 记录文件类型
                if "#" in line and type_flag == 0:
                    if ("TS" in line) or ("ts" in line):
                        type = "TS"
                        type_flag = 1
                    elif ("OPT" in line) or ("opt" in line):
                        type = "OPT"
                        type_flag = 1
                    else:
                        type = "Unknown"
                    if ("ModRedundant" in line) or ("modredundant" in line) or ("maxpoints" in line):
                        type = "Unknown"
                        type_flag = 1
                # 记录文件电荷和自旋多重度，有的文件有bug，居然没对齐！！！
                if "Multiplicity" in line:
                    line_list = list(line.strip().split(" "))
                    if len(line_list) == 6:
                        charge = line_list[2]
                        multiplicity = line_list[5]
                    elif len(line_list) == 7:
                        charge = line_list[3]
                        multiplicity = line_list[6]
                    else:
                        charge = 0
                        multiplicity = 1                        
                count += 1
            coordinates.append([type,charge,multiplicity])
        print("文件{}坐标查找完毕\n".format(self.filename))
        return coordinates

    def get_rocbs_energy(self):
        """查找DL-ROCBS-Q的能量"""
        cbs_energy_list = [0]*(len(self.rocbs_key)+1) # 加上总计值 
        flag = 0
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            for line in file_lines:
                if self.rocbs_key[0] in line and flag == 0: # MP4
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[0] = (self.str_to_digit(energy))
                    flag = 1
                if self.rocbs_key[1] in line and flag == 1 and len(line) < 30: # CCSD
                    energy = list(line.strip().split("= "))[-1]
                    cbs_energy_list[1] = (self.str_to_digit(energy))      
                if "Normal termination" in line and flag != 3 and flag != 4:
                    flag = 2             
                if self.rocbs_key[2] in line and flag == 2: # MP2
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[2] = (self.str_to_digit(energy))
                    flag = 3   
                if self.rocbs_key[3] in line and flag == 3: # MP4
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[3] = (self.str_to_digit(energy))
                if "Normal termination" in line and flag != 2:
                    flag = 4   
                if self.rocbs_key[4] in line and flag == 4: # hf
                    energy = list(line.strip().split(" "))[6]
                    cbs_energy_list[4] = (float(energy))
                    flag = 5    
                if self.cbs_key[5] in line and flag == 5: # INT
                    energy = list(line.strip().split(" "))
                    e2_cbs = float(energy[6])
                    cbs_int = float(energy[14])
                    cbs_energy_list[5] = (e2_cbs + cbs_int)
                    flag = 6                    
                if self.cbs_key[6] in line and flag == 6: # OIII
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[6] = (float(energy))
                    break
                if self.cbs_key[7] in line: # T1 value
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[7] = (float(energy))

        delta_ccsd = cbs_energy_list[1] - cbs_energy_list[0] 
        delta_cbs = cbs_energy_list[3] - cbs_energy_list[2] 
        mp2 = cbs_energy_list[4] + cbs_energy_list[5] - cbs_energy_list[6]*0.00579
        final_energy = round((delta_ccsd + delta_cbs + mp2), 6)
        cbs_energy_list[8] = (final_energy)  

        print("文件{}cbs能量查找完毕\n".format(self.filename))
        return cbs_energy_list

    def get_cbs_sp_energy(self):
        """查找一步的CBS-SP的能量,返回一个查询完的列表 """
        energy_list = [0] 
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            for line in file_lines:
                if "E(CBS-QB3)=" in line:
                    energy_list[0] = float(line.split()[1])
                    # break

        print("文件{}能量查找完毕\n".format(self.filename))
        return energy_list

    def str_to_digit(self, str_cont):
        """Converts a string with letter D+- to a digit"""
        cont_list = list(str_cont.strip().split("D+"))
        return round((float(cont_list[0])*10**int(cont_list[1])),6)

    def str_list_to_2float(self, str_list):
        """Converts a string list to a digit"""
        ret_list = []
        for num in str_list:
            ret_list.append(str(round(float(num),2)))
        return ret_list

    def get_cbs_energy(self):
        """查找CBS-QB3能量"""
        cbs_energy_list = [0]*(len(self.rocbs_key)+1) 
        flag = 0
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            for line in file_lines:
                if self.cbs_key[0] in line and flag == 0: # MP4
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[0] = (self.str_to_digit(energy))
                    flag = 1
                if self.cbs_key[1] in line and flag == 1 and len(line) < 30: # CCSD
                    energy = list(line.strip().split("= "))[-1]
                    cbs_energy_list[1] = (self.str_to_digit(energy))      
                if "Normal termination" in line and flag != 3 and flag != 4:
                    flag = 2             
                if self.cbs_key[2] in line and flag == 2: # MP2
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[2] = (self.str_to_digit(energy))
                    flag = 3   
                if self.cbs_key[3] in line and flag == 3: # MP4
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[3] = (self.str_to_digit(energy))
                if "Normal termination" in line and flag != 2:
                    flag = 4   
                if self.cbs_key[4] in line and flag == 4: # hf
                    energy = list(line.strip().split(" "))[6]
                    cbs_energy_list[4] = (float(energy))
                    flag = 5    
                if self.cbs_key[6] in line and flag == 5: # INT
                    energy = list(line.strip().split(" "))
                    e2_cbs = float(energy[6])
                    cbs_int = float(energy[14])
                    cbs_energy_list[5] = (e2_cbs + cbs_int)
                    flag = 6                    
                if self.cbs_key[5] in line and flag == 6: # OIII
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[6] = (float(energy))
                    break
                if self.cbs_key[7] in line: # T1 value
                    energy = list(line.strip().split(" "))[-1]
                    cbs_energy_list[7] = (float(energy))

        delta_ccsd = cbs_energy_list[1] - cbs_energy_list[0] 
        delta_cbs = cbs_energy_list[3] - cbs_energy_list[2] 
        mp2 = cbs_energy_list[4] + cbs_energy_list[5] - cbs_energy_list[6]*0.00579
        final_energy = round((delta_ccsd + delta_cbs + mp2), 6)
        cbs_energy_list[8] = (final_energy)    
        print("文件{}cbs能量查找完毕\n".format(self.filename))
        return cbs_energy_list

    def check_OK(self):
        """检查是否存在YES """
        pass
    
    def eigenvectors(self, count = 300):
        """检查未完成任务中的虚频，直接打印，不需要储存"""
        # 经过一步只输出一个虚频
        content_list = []
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            show = 0
            for line_num in range(len(file_lines)):
                if count <= 0:
                    break
                if "Step number" in file_lines[line_num]:
                    show = 1
                    count -= 1
                    #print("\n{}".format((file_lines[line_num]).strip()))
                    content_list
                if "Eigenvalues ---" in file_lines[line_num] and show == 1:
                    #print((file_lines[line_num]).strip())
                    content_list.append((file_lines[line_num]).strip())
                    content_list
                    show = 0
                if "Eigenvectors" in file_lines[line_num]:
                    content_list.append((file_lines[line_num+1]).strip())
                    content_list.append(file_lines[line_num+2].strip()[-48:])
                    #print((file_lines[line_num+1]).strip())
                    #print(file_lines[line_num+2].strip()[-48:])

        return content_list
                    
    def eigenvectors_YES(self, count = 300):
        """检查未完成任务中的虚频，直接打印，不需要储存"""
        """检查是否存在YES """
        # 经过一步只输出一个虚频
        content_list = []
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            show = 0
            for line_num in range(len(file_lines)):
                if count <= 0:
                    break
                if "Step number" in file_lines[line_num]:
                    show = 1
                    count -= 1
                    #print("\n{}".format((file_lines[line_num]).strip()))
                    content_list.append("\n{}".format((file_lines[line_num]).strip()))
                if "Eigenvalues ---" in file_lines[line_num] and show == 1:
                    #print((file_lines[line_num]).strip())
                    content_list.append((file_lines[line_num]).strip())
                    show = 0
                if "Eigenvectors" in file_lines[line_num]:
                    #print((file_lines[line_num+1]).strip())
                    #print(file_lines[line_num+2].strip()[-48:])
                    content_list.append((file_lines[line_num+1]).strip())
                    content_list.append(file_lines[line_num+2].strip()[-48:])
                for YES_key in self.YES_keys:
                    if "YES" in file_lines[line_num] and YES_key in file_lines[line_num]:
                        #print(file_lines[line_num].strip())
                        content_list.append(file_lines[line_num].strip())

        return content_list
                
if __name__ == "__main__":
    energy_dict_test = {}
    A= FindInfo(r"E:\Research\AP\task-1130\二茂铁-AP\FeR2\Rate\R\2.log")
    print(A.get_others())
    # print(A.get_rocbs_energy())
        


