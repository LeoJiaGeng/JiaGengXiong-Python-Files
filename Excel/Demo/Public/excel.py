'''只为做一些小实用程序
'''
import xlrd
import xlwt
from Public.decoration import Decorator
import pandas as pd

class Excels():
    '''excel表格读写的操作'''

    def __init__(self):
        pass
    
    @Decorator.exe_time("读取excel")
    def read_excel_lines(self, filename, search_list, direction = 0, sheet_index = 0, get_start_rowx = 0, get_end_rowx = None):
        '''读取表格中的某些行、列'''
        print(f"开始读取{filename}文件")

        data = xlrd.open_workbook(r"" + filename)
        sheet = data.sheet_by_index(sheet_index)
        read_list = []

        for i in range(len(search_list)):
            if direction == 0:
                # 读取行
                read_list.append(sheet.col_values(search_list[i], start_rowx = get_start_rowx, end_rowx = get_end_rowx))
            elif direction == 1:
                # 读取列
                read_list.append(sheet.row_values(search_list[i], start_colx = get_start_rowx, end_colx = get_end_rowx))   
            else:
                print("输入有误") 
                break           

        print(f"{filename}文件已经读取完毕")
        return read_list

    @Decorator.exe_time("写入excel")
    def write_excel_lines(self, get_list, direction = 0, filename = "提取的源文件.xls", set_start_row = 0, set_start_col = 0):
        workbook = xlwt.Workbook(encoding = 'utf-8')
        sheet = workbook.add_sheet('sheet0')
        
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
                    # 写入行
                    sheet.write(set_start_row + row, set_start_col + col, get_list[row][col])  
                elif direction == 1:
                    # 写入列
                    sheet.write(set_start_row + col, set_start_col  + row, get_list[row][col])
                else:
                    print("写入方向输入有误") 
        
        workbook.save(filename)    

    @Decorator.exe_time("csv转换xlsx")
    def csv_to_excel(self, csv_filename, xlsx_filename):
        pd.read_csv(csv_filename).to_excel(xlsx_filename, index=False)

    @Decorator.exe_time("txt转换xlsx")
    def txt_to_excel(self, column_index):
        pd.read_table("file.txt", sep=" ", header=None, names=column_index).to_excel("file.xlsx", index=False)

if __name__ == "__main__":
    file_name = r"D:\Document\宝儿临时文件夹\副本广建大酒店三月收支.xlsx" 
    A = Excels()
    print(A.read_excel_lines(file_name, [3,4], direction=0))
    A.write_excel_lines([[1,2,5,67,5],[3,4],[4,5,6]], direction=1)
