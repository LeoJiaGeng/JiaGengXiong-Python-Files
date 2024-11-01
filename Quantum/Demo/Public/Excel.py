import xlrd
import xlwt
import pandas as pd

from Public.decoration import Decorator

class Excels():
    '''excel表格读写的操作'''

    def __init__(self):
        pass

    @Decorator.raise_err()
    def read_excel_lines(self, filename, search_list, direction = 0, sheet_index = 0, get_start_rowx = 0, get_end_rowx = None):
        '''输入: 1.文件名的绝对地址; 2.查找行/列的数组; 3.查找的方向; 4.表格的sheet
           输出: 1.状态值; 2.二维数组; 3.过程信息'''
        
        ret = {"ret_val":True, "data":[], "info":"normal operation"}

        data = xlrd.open_workbook(r"" + filename)
        sheet = data.sheet_by_index(sheet_index)

        for one_list in search_list:
            if direction == 0:
                # 读取行
                ret["data"].append(sheet.col_values(one_list, start_rowx = get_start_rowx, end_rowx = get_end_rowx))
            elif direction == 1:
                ret["data"].append(sheet.row_values(one_list, start_colx = get_start_rowx, end_colx = get_end_rowx))   
            else:
                ret["ret_val"] = False
                ret["info"] = "input direction is wrong"
                return ret                   

        return ret

    @Decorator.raise_err()
    def write_excel_lines(self, get_list, direction = 0, filename = "提取的源文件.xls", set_start_row = 0, set_start_col = 0):
        '''输入: 1.二维数组; 2.写入的方向; 3.新建的文件名; 
           输出: 1.状态值; 2.空数组; 3.过程信息'''
        
        ret = {"ret_val":True, "data":[], "info":"normal operation"}

        workbook = xlwt.Workbook(encoding = 'utf-8')
        sheet = workbook.add_sheet('sheet0')

        # 设置列宽
        sheet.col(0).width = 20 * 256 # 256是列宽的基本单位，20个字符宽度
        for i in range(1, 6):
            sheet.col(i).width = 13 * 256 # 256是列宽的基本单位，12个字符宽度
        # 设置行高
        # sheet.row(0).height_mismatch = True  # 允许行高不匹配
        sheet.row(0).height = 12 * 20  # 设置第一行高度为30点      

        # 进行对齐，这个是格式
        alignment = xlwt.Alignment() # Create Alignment
        alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
        style = xlwt.XFStyle() # Create Style
        style.alignment = alignment # Add Alignment to Style

        row_length = len(get_list)
        for row in range(row_length): 
            for col in range(len(get_list[row])):     
                if direction == 0:
                    sheet.write(set_start_row + row, set_start_col + col, get_list[row][col]) # 写入行
                elif direction == 1:
                    sheet.write(set_start_row + col, set_start_col + row, get_list[row][col]) # 写入列
                else:
                    ret["info"] = "input direction is wrong"
                    return ret 
        
        workbook.save(filename)
        return ret    

    @Decorator.raise_err()
    def csv_to_excel(self, csv_filename, xlsx_filename):
        '''输入: 1.csv文件绝对地址; 2.xlsx的绝对地址; 
           输出: 1.状态值; 2.空数组; 3.过程信息'''
        ret = {"ret_val":True, "data":[], "info":"normal operation"}
        pd.read_csv(csv_filename).to_excel(xlsx_filename, index=False)
        return ret

    @Decorator.raise_err()
    def txt_to_excel(self, column_index):
        '''输入: 1.xlsx的文件头; 
           输出: 1.状态值; 2.空数组; 3.过程信息'''
        ret = {"ret_val":True, "data":[], "info":"normal operation"}
        pd.read_table("file.txt", sep=" ", header=None, names=column_index).to_excel("file.xlsx", index=False)
        return ret
    
if __name__ == "__main__":
    file_name = r"D:\桌面文件夹\代码测试\测试文件\1.xlsx" 
    A = Excels()
    ret = A.read_excel_lines(file_name, [1,2], direction=1)
    if not (ret["ret_val"]):
        print(ret["info"])
    else:
        print(ret["data"])
    print(A.txt_to_excel())
    print(A.write_excel_lines([[1,2,5,5],[3,4],[4,5,6]], direction=1))
