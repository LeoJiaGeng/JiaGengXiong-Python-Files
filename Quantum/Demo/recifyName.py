from Public.Files import ReFilenames

class RecifyName():
    def __init__(self):
        pass
    
    def del_filename(self, file_path, del_type, str_num1, str_num2=None, transfer = True):
        old_filename = []
        new_filename = []
        new_raw_name = ""
        # 实例化ReFilenames类
        rf = ReFilenames()
        abs_filepath_list = rf.get_all_files_in_folder(file_path)
        for abs_filepath in abs_filepath_list:
            file_foler, file_name, raw_name, file_suf = rf.get_file_detail(abs_filepath)
            old_filename.append(raw_name)
            # 判断文件名长度是否小于str_num，若小于则跳过
            if (len(raw_name) <= str_num1) and (str_num2 is not None and len(raw_name) >= str_num1+str_num2):
                print('raw_name length is less than str_num')
                continue
            if del_type == 'PRE':
                new_raw_name = raw_name[str_num1:]
            elif del_type =='SUF':
                new_raw_name = raw_name[:-str_num1]
            elif del_type == 'BOTH':
                new_raw_name = raw_name[str_num1:-str_num2]
            elif del_type == 'MED':
                new_raw_name = raw_name[:str_num1] + raw_name[str_num2:] 
            else:
                print('del_type error')
            # 重命名文件
            if transfer:
                rf.rename_file(abs_filepath, rf.combine_file(file_foler, new_raw_name, file_suf))
            else:
                new_filename.append(new_raw_name)
        if not transfer:
            return old_filename, new_filename

    def add_filename(self, file_path, add_type, add_str, add_str_loc=0, transfer = True):
        old_filename = []
        new_filename = []
        new_raw_name = ""
        # 实例化ReFilenames类
        rf = ReFilenames()
        abs_filepath_list = rf.get_all_files_in_folder(file_path)
        for abs_filepath in abs_filepath_list:
            file_foler, file_name, raw_name, file_suf = rf.get_file_detail(abs_filepath)
            old_filename.append(raw_name)
            # 判断文件名长度是否小于add_str_loc，若小于则跳过
            if (len(raw_name) < add_str_loc):
                print('raw_name length is less than add_str_loc')
                continue
            if add_type == 'PRE':
                new_raw_name = add_str + raw_name
            elif add_type =='SUF':
                new_raw_name = raw_name + add_str 
            elif add_type == 'MED':
                new_raw_name = raw_name[:add_str_loc] + add_str + raw_name[add_str_loc:] 
            elif add_type == 'BOTH':
                new_raw_name = raw_name # 暂时不变，防止出现意外！！！
            else:
                print('add_type error')
            # 重命名文件
            if transfer:
                rf.rename_file(abs_filepath, rf.combine_file(file_foler, new_raw_name, file_suf))
            else:
                new_filename.append(new_raw_name)
        if not transfer:
            return old_filename, new_filename

if __name__ == '__main__':
    rf = RecifyName()
    # rf.del_filename(r"C:\Users\DELL\Desktop\SO2F\all-cal-data\extract\avdz - 副本", 'suf', 4)
    rf.add_filename(r"C:\Users\DELL\Desktop\SO2F\all-cal-data\extract\avdz - 副本", 'suf', "-avdz")

