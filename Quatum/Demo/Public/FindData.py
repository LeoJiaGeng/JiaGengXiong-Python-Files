"""
查找log文件文件里面的零点能、吉布斯、HF的能量和虚频以及YES，返回数组!!!
"""

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
        
        energy_list[2] = float(energy_list[3]) - float(energy_list[1])
        energy_check_count += 1
        energy_list[4] = energy_list[2] + energy_list[0]
        energy_check_count += 1
        print("文件{}能量查找完毕\n".format(self.filename))
        # 进行文件检查
        if self.energy_check(energy_list, energy_check_count):
            return energy_list
        else:
            return [0] * len(self.energy_key_word)

    def get_freq(self):
        """查找振动频率"""
        freq_list = []
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            for line in file_lines:
                if self.freq_key[0] in line and self.freq_key[1] not in line:
                    line = line.strip()
                    line = line.split(" ")
                    tran_list = [item for item in line if len(item.split(".")) == 2]
                    freq_list.extend(tran_list)
               
        print("文件{}频率查找完毕\n".format(self.filename))
        if freq_list == []:
            print("未找到能量数据")
        return freq_list

    def get_coord(self):
        """查找坐标"""
        coordinates = []
        # 遇到恢复词，不写入，直接终止循环
        # 遇到冗余内坐标开始记录
        with open(self.filename, mode="r", buffering=-1, encoding="utf-8") as fileObj:
            file_lines = fileObj.readlines()
            start = 0
            for line in file_lines:
                if self.coordinates_key[1] in line:
                    break            
                if start == 1:
                    line = line.strip()
                    coordinates.append(line)
                if self.coordinates_key[0] in line:
                    start = 1

        print("文件{}坐标查找完毕\n".format(self.filename))
        return coordinates

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
    A= FindInfo(r"D:\data\C2F2O\C2F2_1.log")
    print(A.eigenvectors_YES())


