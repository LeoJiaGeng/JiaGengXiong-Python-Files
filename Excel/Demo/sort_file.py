'''将文件夹内多个表格中的某些行或者列按顺序整合到一起
'''
from Public.excel import Excels
from Public.files import ReFilenames

class SortFiles(object):
    def __init__(self):
        self.excel = Excels()
        pass

    def main_function(self, name_type, file_name, list_num, read_type, write_type, sheet_num = 0, row_start_num = 0):
        root = ReFilenames(name_type)
        all_data = [] 

        all_file_names = root.get_all_files(file_name) # 默认是全路径
        for name in all_file_names:  # 循环所有文件名
            data = self.excel.read_excel_lines(name, list_num, read_type, sheet_num, row_start_num)
            # 获取每个文件中的数据       
            all_data.extend(data)
            
        self.excel.write_excel_lines(all_data, write_type)

    def main_convert(self, file_name):
        root = ReFilenames("csv")
        all_file_full_names = root.get_all_files(file_name) # 默认是全路径
        all_file_names = root.get_all_files(file_name, True) #
        for full_name, name in zip(all_file_full_names,all_file_names):  # 循环所有文件名
            xlsx_name = str(name.split(".")[0]) + ".xlsx"
            self.excel.csv_to_excel(full_name, xlsx_name)        

if __name__ == '__main__':   
    # 主程序开始
    name_type = 'xls'
    # 文件后缀名
    file_name = r'D:\OneDrive\桌面\异构体能量对比'
    # 文件夹目录

    sheet_num = 0
    # 表格中表单序号，默认第一个是表单是0
    list_num = [3]
    # 需要整合的行数或列数的序列，单行可以只写一个数字
    rstart_num = 0
    # 读取时开始的行数和列数，列数默认到没有数据结束

    row_col = 0
    '''这个参数很重要'''
    # 写入行（0）还是列（1）
    col_wstart_num = 0
    row_wstart_num = 0
    # 写入时开始的行数和列数

    # 是否提取数据的部分
    A = SortFiles()
    A.main_function(name_type, file_name, sheet_num, list_num, rstart_num, row_col)




