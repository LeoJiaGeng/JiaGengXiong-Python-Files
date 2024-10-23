# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: jxiong@whu.edu.cn
"""

import sys, os, platform
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt, QThread, pyqtSignal
from enum import Enum  ##枚举类型

from ui_Start import QmyWidget
from quantum import Quantum
from gausInput import GauInput
from recifyName import RecifyName

from Public.config_adapt import Config_Adapt
from Public.Rename import rename, back_folder, recover_folder
from enum import Enum

class CellType(Enum):    ##各单元格的类型
   ct_name=1000
   ct_zpe=1001
   ct_cor_G=1002
   ct_HF=1003
   ct_Gibbs=1004
   ct_Energy=1005
   ct_delta_G=1006
   ct_delta_E=1007

class FieldColNum(Enum):   ##各字段在表格中的列号
    col_name=0
    col_zpe=1
    col_cor_G=2
    col_HF=3
    col_Gibbs=4
    col_Energy=5
    col_delta_G=6
    col_delta_E=7

class QmyApp(QmyWidget):
    def __init__(self): # initialize config file and class parameters
        super().__init__()
        self.save_content_show(f"Python的版本为: {platform.python_version()}")
        self.config_init()
        self.params_init()

##  ========== the function of config files ================== 

    def config_init(self): # read configuration from config file and initialization
        self.config = Config_Adapt("quantum_config.ini")

        self.ui.combo_save_folder.addItem(self.config.get_config("save", "save_folder")["data"])
        self.ui.combo_save_filename.addItem(self.config.get_config("save", "save_file_name")["data"])
        self.ui.edit_standard_G.setText(self.config.get_config("save", "standard_Gdata")["data"])
        self.ui.edit_standard_E.setText(self.config.get_config("save", "standard_Edata")["data"])
        
        self.ui.edit_file.setText(self.config.get_config("search", "search_file_name")["data"])
        
        self.ui.combo_update_folder.addItem(self.config.get_config("transfer", "trans_update_folder")["data"])
        self.ui.edit_trans_folder.setText(self.config.get_config("transfer", "trans_folder_name")["data"])
        self.ui.edit_trans_ruler.setText(self.config.get_config("transfer", "trans_ruler")["data"])
        self.ui.edit_trans_pre.setText(self.config.get_config("transfer", "trans_prefix")["data"])
        self.ui.combo_trans_suf.addItem(self.config.get_config("transfer", "trans_suffix")["data"])

        self.ui.edit_rename_folder.setText(self.config.get_config("rename", "rename_folder")["data"])
        self.ui.edit_rename_loc1.setText(self.config.get_config("rename", "rename_loc1")["data"])
        self.ui.edit_rename_loc2.setText(self.config.get_config("rename", "rename_loc2")["data"])
        self.ui.edit_rename_addstr.setText(self.config.get_config("rename", "rename_addstr")["data"])

    def save_saving_config(self): # store configuration in saving interface
        """Save the content of the line edit in saving window"""
        self.config.set_config("save", "save_folder", self.ui.combo_save_folder.currentText()) 
        self.config.set_config("save", "save_file_name", self.ui.combo_save_filename.currentText())
        self.config.set_config("save", "standard_Gdata", self.ui.edit_standard_G.text())  
        self.config.set_config("save", "standard_Edata", self.ui.edit_standard_E.text()) 
        
    def save_search_config(self): # store configuration in search interface
        """Save the contents of the line edit in searching window"""
        self.config.set_config("search", "search_file_name", self.ui.edit_file.text())

    def save_transfer_config(self): # store configuration in transferring interface
        """Save the contents of the line edit in transferring window"""
        self.config.set_config("transfer", "trans_folder_name", self.ui.edit_trans_folder.text())
        self.config.set_config("transfer", "trans_ruler", self.ui.edit_trans_ruler.text())
        self.config.set_config("transfer", "trans_update_folder", self.ui.combo_update_folder.currentText())
        self.config.set_config("transfer", "trans_prefix", self.ui.edit_trans_pre.text())
        self.config.set_config("transfer", "trans_suffix", self.ui.combo_trans_suf.currentText())

    def save_rename_config(self): # store configuration in renaming interface
        """Save the contents of the line edit in renaming window"""
        self.config.set_config("rename", "rename_folder", self.ui.edit_rename_folder.text())
        self.config.set_config("rename", "rename_loc1", self.ui.edit_rename_loc1.text())
        self.config.set_config("rename", "rename_loc2", self.ui.edit_rename_loc2.text())
        self.config.set_config("rename", "rename_addstr", self.ui.edit_rename_addstr.text())

##  ========== the function of params ================== 

    def params_init(self):
        self.ui.tableInfo.setAlternatingRowColors(True) # Alternate color for table 
        self.energy_list = [] # receiving energy list
        self.freq_list = [] # receiving frequency list

##  ========== the function of saving window ==================  
     
    def insert_combo(self, combo_name, insert_str):
	# insert str at the first in the combox, and refresh the combox list
        read_data_list = []
        for i in range(combo_name.count()):
            read_data_list.append(combo_name.itemText(i))
        if insert_str not in read_data_list:
            read_data_list.insert(0, insert_str)
            combo_name.clear()
            combo_name.addItems(read_data_list)

    @pyqtSlot()
    def on_btn_save_clear_clicked(self): # clear saving interface
        self.save_content_clear()

    @pyqtSlot()
    def on_btn_table_clear_clicked(self): # clear table showing
        self.table_content_clear()
    
    @pyqtSlot()
    def on_btn_open_folder_clicked(self): # select a folder not save configuration
        selectedDir = self.open_folder()
        if selectedDir:
            self.insert_combo(self.ui.combo_save_folder, selectedDir)

    @pyqtSlot()
    def on_btn_save_energy_clicked(self): # save energy button and configuration
        try:
            self.save_content_show("Saving energy... ...")
            folder_name = self.ui.combo_save_folder.currentText()
            self.quant = Quantum("log",folder_name, self.ui.edit_standard_G.text(), self.ui.edit_standard_E.text())
            write_file_name = self.ui.combo_save_filename.currentText() + ".xls"
            write_file_path = os.path.join(folder_name, write_file_name)
            self.energy_list = self.quant.save_energy(write_file_path)
            os.startfile(write_file_path) # open the file with default application
            self.save_content_show("Save OK!")
            self.save_saving_config()
            self.table_show(True)
        except Exception as e:
            self.save_content_show(str(e))
            self.save_content_show("Save ERR!")

    @pyqtSlot()
    def on_btn_save_cbs_energy_clicked(self): # save cbs energy button and configuration
        try:
            self.save_content_show("Saving cbs energy... ...")
            folder_name = self.ui.combo_save_folder.currentText()
            self.quant = Quantum("log",folder_name, self.ui.edit_standard_G.text(), self.ui.edit_standard_E.text())
            write_file_name = self.ui.combo_save_filename.currentText() + ".xls"
            write_file_path = os.path.join(folder_name, write_file_name)
            if self.ui.chebox_one_step.isChecked():
                self.energy_list = self.quant.save_cbs_energy(write_file_path, "ONE_LINK")
                self.save_content_show("Save OK! BUT NOT SHOW IN THE TABLE !!!")
            else:
                self.energy_list = self.quant.save_cbs_energy(write_file_path, "MULTI_LINKS")
                self.table_show(True)
                self.save_content_show("Save OK!")
            self.save_saving_config()
        except Exception as e:
            self.save_content_show(str(e))
            self.save_content_show("Save ERR!")

    @pyqtSlot()
    def on_btn_save_freq_clicked(self):  # save frequency button and configuration
        try:
            self.save_content_show("Saving frequency... ...")
            folder_name = self.ui.combo_save_folder.currentText()
            self.quant = Quantum("log",folder_name)
            write_file_name = self.ui.combo_save_filename.currentText() + ".docx"
            write_file_path = os.path.join(folder_name, write_file_name)
            self.freq_list = self.quant.save_freq(write_file_path)
            self.save_content_show("Save OK!")
            self.save_saving_config()
            self.table_show(False)
        except Exception as e:
            self.save_content_show(str(e))
            self.save_content_show("Save ERR!")

    @pyqtSlot()
    def on_btn_save_coord_clicked(self): # save coordinate button and configuration
        try:
            self.save_content_show("Saving coordinates... ...")
            folder_name = self.ui.combo_save_folder.currentText()
            self.quant = Quantum("log",folder_name)
            write_file_name = self.ui.combo_save_filename.currentText() + ".docx"
            write_file_path = os.path.join(folder_name, write_file_name)
            self.quant.save_cor(write_file_path)
            self.save_content_show("Save OK!")
            self.save_saving_config()
        except Exception as e:
            self.save_content_show(str(e))
            self.save_content_show("Save ERR!")

    @pyqtSlot()
    def on_btn_table_clear_clicked(self): # clear saving interface
        self.ui.tableInfo.clearContents()

    def set_table_header(self, header_text = ["文件名"]): # set table header
        self.ui.tableInfo.setColumnCount(len(header_text))
        self.ui.tableInfo.setHorizontalHeaderLabels(header_text)

    def table_show(self, energy): # show table
        self.table_content_clear()
        row_num = 0
        if energy:
            for row_list in self.energy_list:
                self.ui.tableInfo.insertRow(row_num)
                name = row_list[FieldColNum.col_name.value]
                zpe = row_list[FieldColNum.col_zpe.value]
                cor_G = row_list[FieldColNum.col_cor_G.value]
                hf = row_list[FieldColNum.col_HF.value]
                Gibbs = row_list[FieldColNum.col_Gibbs.value]
                Energy = row_list[FieldColNum.col_Energy.value]
                delta_G = row_list[FieldColNum.col_delta_G.value]
                delta_E = row_list[FieldColNum.col_delta_E.value]
                self.__createItemsARow(row_num,name,zpe,cor_G,hf,Gibbs,Energy,delta_G,delta_E)
                row_num += 1
        else:
            for row_list in self.freq_list:
                self.ui.tableInfo.insertRow(row_num)
                name = row_list[FieldColNum.col_name.value]
                freq = row_list[FieldColNum.col_zpe.value]
                self.__createItemsARow(row_num,name,freq,0,0,0,0,0,0)
                row_num += 1

    def __createItemsARow(self,rowNo,name,zpe,cor_G,hf,Gibbs,Energy,delta_G,delta_E): ## create items in a row
        str_content=str(name)
        item=QTableWidgetItem(str_content,CellType.ct_name.value)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_name.value,item)

        str_content=str(zpe)
        item=QTableWidgetItem(str_content,CellType.ct_zpe.value)
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_zpe.value,item)

        str_content=str(cor_G)
        item=QTableWidgetItem(str_content,CellType.ct_cor_G.value)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_cor_G.value,item)

        str_content=str(hf)
        item=QTableWidgetItem(str_content,CellType.ct_HF.value)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_HF.value,item)

        str_content=str(Gibbs)
        item=QTableWidgetItem(str_content,CellType.ct_Gibbs.value)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_Gibbs.value,item)

        str_content=str(Energy)
        item=QTableWidgetItem(str_content,CellType.ct_Energy.value)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_Energy.value,item)

        str_content=str(delta_G)
        item=QTableWidgetItem(str_content,CellType.ct_delta_G.value)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_delta_G.value,item)

        str_content=str(delta_E)
        item=QTableWidgetItem(str_content,CellType.ct_delta_E.value)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableInfo.setItem(rowNo,FieldColNum.col_delta_E.value,item)

    @pyqtSlot(bool)
    def on_btn_auto_adapt_clicked(self, checked):
        self.ui.tableInfo.resizeRowsToContents() # resize rows
        self.ui.tableInfo.resizeColumnsToContents() # resize columns
        self.ui.tableInfo.horizontalHeader().setVisible(checked)  # show h_header 
        self.ui.tableInfo.verticalHeader().setVisible(checked) # show v_header

    @pyqtSlot(str)
    def on_comboBox_currentIndexChanged(self, text): # change combobox
        pass



##  ========== the function of searching window ==================  
            
    @pyqtSlot()
    def on_btn_open_file_clicked(self): # select a file not save configuration
        fileList, filt = self.open_file()
        self.ui.edit_file.setText(fileList)

    @pyqtSlot()
    def on_btn_find_ver_clicked(self): # find eigenvector for gaussian output file and save configuration
        try:
            self.search_content_show("Searching eigenvectors... ...")
            file_name = self.ui.edit_file.text()
            self.quant = Quantum("log",file_name)

            for content in self.quant.print_eigenvectors():
                self.search_content_show(content)
            self.search_content_show("Search OK!")
            self.save_search_config()
        except Exception as e:
            self.search_content_show(str(e))
            self.search_content_show("Search ERR!")

    @pyqtSlot()
    def on_btn_find_yes_clicked(self): # find yes for gaussian output file and save configuration 
        try:
            self.search_content_show("Searching eigenvectors... ...")
            file_name = self.ui.edit_file.text()
            self.quant = Quantum("log",file_name)

            for content in self.quant.print_eigenvectors_YES():
                self.search_content_show(content)
            self.search_content_show("Search OK!")
            self.save_search_config()
        except Exception as e:
            self.search_content_show(str(e))
            self.search_content_show("Search ERR!")

    def on_btn_clear_clicked(self): # clear searching interface
        self.ui.search_plainTextEdit.clear()

#========== the function of transferring window ==================

    @pyqtSlot()
    def on_btn_sel_file_clicked(self): # select a folder save configuration and list files name
        selectedDir = self.open_folder()
        if selectedDir != "":
            self.insert_combo(self.ui.combo_update_folder, selectedDir)
            self.save_transfer_config()
        # requirement: when give it up , keep old recoder 

    @pyqtSlot()
    def on_btn_creat_gauinput_clicked(self): # set gaussian input
        folder = self.ui.combo_update_folder.currentText()
        gausiput_obj = GauInput()
        pre = self.ui.edit_trans_pre.text()
        suf = self.ui.combo_trans_suf.currentText()
        if (self.ui.radbtn_chalevel.isChecked()):
            execType = "Unknow"
        elif (self.ui.radbtn_fullirc.isChecked()):
            execType = "IRC"
        elif (self.ui.radbtn_apartirc.isChecked()):
            execType = "IRC-SPLIT"
        elif (self.ui.radbtn_frozopt.isChecked()): # 功能有问题，待修复
            execType = "F-OPT"
        elif (self.ui.radbtn_highsp.isChecked()):
            execType = "HIGH-SP"

        read_file_type = self.ui.combo_trans_read_type.currentText()
        gausiput_obj.create_gjfs(foldername=folder, prefix = pre, suffix = suf, file_type=execType, read_type=read_file_type)   
        self.trans_log_show("文件创建成功！")
        self.save_transfer_config() # save configuration after success

    @pyqtSlot()
    def on_btn_trans_open_folder_clicked(self): # select a folder save configuration and list files name
        self.ui.plainTextEdit_trans_origin.clear()
        selectedDir = self.open_folder()
        if selectedDir != "":
            self.ui.edit_trans_folder.setText(selectedDir)
            self.show_trans_origin_content()
        self.save_transfer_config()

    def show_trans_origin_content(self): # show origin content
        folder = self.ui.edit_trans_folder.text()
        self.origin_name_list = [name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder,name))] 
        for name in self.origin_name_list:
            self.trans_origin_content_show(name)

    @pyqtSlot()
    def on_btn_transfer_clicked(self): # show the process of transfer 
        try:
            self.back_temp = back_folder(self.ui.edit_trans_folder.text())
            self.trans_log_show("文件已备份！")
            rename(self.ui.edit_trans_folder.text(), self.origin_name_list, self.new_name_list)
            for i, j in zip(self.origin_name_list, self.new_name_list):
                log_content = i + " --> " + j
                self.trans_log_show(log_content)
            self.save_transfer_config()
        except Exception as e:
            self.trans_log_show(str(e))

    @pyqtSlot()
    def on_btn_trans_refresh_clicked(self): # only refresh original window
        self.trans_origin_content_clear()
        try:
            self.show_trans_origin_content()
        except Exception as e:
            self.trans_log_show(str(e))

    @pyqtSlot()
    def on_btn_trans_clear_clicked(self): # clear all windows
        self.ui.plainTextEdit_trans_origin.clear()
        self.ui.plainTextEdit_trans_new.clear()
        self.ui.plainTextEdit_trans_log.clear()

    @pyqtSlot()
    def on_btn_check_new_name_clicked(self): # show new name list in the new window
        try:
            self.ui.plainTextEdit_trans_new.clear() 
            ruler_list = list(self.ui.edit_trans_ruler.text().split(','))
            self.new_name_list = []
            for ruler in ruler_list:
                file_name = ruler.strip().split(" ")[0]
                time = ruler.strip().split(" ")[1]
                for i in range(int(time)):
                    self.new_name_list.append(file_name)
                    self.trans_new_content_show(file_name)
            self.save_transfer_config()
        except Exception as e:
            self.trans_log_show(str(e))

    @pyqtSlot()
    def on_btn_trans_retract_clicked(self): # refresh next time
        try:
            old_folder = self.ui.edit_trans_folder.text()
            recover_folder(self.back_temp, old_folder)
            self.trans_log_show(f"文件夹从{self.back_temp}成功恢复到{old_folder}！")
        except Exception as e:
            self.trans_log_show(str(e))

# ========== the function of rename window ==================
    def rename_read_params(self): # read parameters from the rename window
        if (self.ui.edit_rename_loc1.text() == ""):
            self.edit_rename_loc1 = 0
        else:
            self.edit_rename_loc1 = int(self.ui.edit_rename_loc1.text())

        if (self.ui.edit_rename_loc2.text() == ""):
            self.edit_rename_loc2 = 0
        else:
            self.edit_rename_loc2 = int(self.ui.edit_rename_loc2.text())

        self.rename_folder = self.ui.edit_rename_folder.text()
        self.rename_add_str = self.ui.edit_rename_addstr.text()
        self.rf = RecifyName()
        if (self.ui.radbtn_pre.isChecked()):
            self.ref_type = "PRE"
        elif (self.ui.radbtn_suf.isChecked()):
            self.ref_type = "SUF"
        elif (self.ui.radbtn_med.isChecked()):
            self.ref_type = "MED"
        elif (self.ui.radbtn_both.isChecked()):
            self.ref_type = "BOTH"
        else:
            print("error")
            self.ui.plainTextEdit_rename_log.appendPlainText("传入参数有误！")
            return 0

    def rename_func(self, rename_type = "DEL", transfer_type = True):  # create rename window
        self.rename_read_params() # read parameters frist
        self.save_rename_config() # save parameters later

        if (rename_type == "DEL"):
            if transfer_type:
                self.rf.del_filename(self.rename_folder, self.ref_type, self.edit_rename_loc1, self.edit_rename_loc2)
                self.ui.plainTextEdit_rename_log.appendPlainText("删除文件名已完成！")
            else:
                return self.rf.del_filename(self.rename_folder, self.ref_type, self.edit_rename_loc1, self.edit_rename_loc2, False)

        elif (rename_type == "ADD"):
            if transfer_type:
                self.rf.add_filename(self.rename_folder, self.ref_type, self.rename_add_str, self.edit_rename_loc1)
                self.ui.plainTextEdit_rename_log.appendPlainText("增加文件名已完成！") 
            else:
                return self.rf.add_filename(self.rename_folder, self.ref_type, self.rename_add_str, self.edit_rename_loc1, False)       
        else:
            print("error")
            self.ui.plainTextEdit_rename_log.appendPlainText("传入参数有误！") 
            return 0  
        
    @pyqtSlot()
    def on_btn_rename_open_folder_clicked(self): # select a folder not save configuration
        selectedDir = self.open_folder()
        self.ui.edit_rename_folder.setText(selectedDir)
        self.config.set_config("rename", "rename_folder", self.ui.edit_rename_folder.text())

    @pyqtSlot()
    def on_btn_rename_refresh_clicked(self): # refresh the file list to reflect changes
        if (self.ui.radbtn_del.isChecked()):
            check_type = "DEL"
        elif (self.ui.radbtn_add.isChecked()):
            check_type = "ADD"
        else:
            print("error")
            self.ui.plainTextEdit_rename_log.appendPlainText("传入参数有误！")
            return 0
        old_list, new_list = self.rename_func(check_type, False)
        self.ui.plainTextEdit_rename_check.clear()
        for i, j in zip(old_list, new_list):
            log_content = i + "  ----->  " + j
            self.ui.plainTextEdit_rename_check.appendPlainText(log_content)
        self.ui.plainTextEdit_rename_log.appendPlainText("文件名预览，请检查！！！！！\n")

    @pyqtSlot()
    def on_btn_rename_del_clicked(self): # delete file name
        try:
            self.rename_func("DEL")
        except Exception as e:
            self.ui.plainTextEdit_rename_log.appendPlainText(str(e))
        
    @pyqtSlot()
    def on_btn_rename_add_clicked(self):  # add file name
        try:
            self.rename_func("ADD")
        except Exception as e:
            self.ui.plainTextEdit_rename_log.appendPlainText(str(e))

# ========== the function of test window ==================
    @pyqtSlot()
    def on_btnTest_clicked(self): 
        route = self.ui.lineTest.text() 
        # cmd = "kindia.exe surface.xyz 1 2000 "
        print(os.system(route))
        self.ui.exe_plainTextEdit.appendPlainText("指令1运行已完成")

    @pyqtSlot()
    def on_btnTest_2_clicked(self): 
        route = self.ui.lineTest_2.text() 
        print(os.system(route))
        self.ui.exe_plainTextEdit.appendPlainText("指令2运行已完成")

    @pyqtSlot()
    def on_btnTest_3_clicked(self): 
        route = self.ui.lineTest_3.text() 
        print(os.system(route))
        self.ui.exe_plainTextEdit.appendPlainText("指令3运行已完成")

class QuaThread(QThread): # create thread
    sinOut = pyqtSignal(str)  

    def __init__(self):
        super().__init__()
        pass

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyApp()
    myWidget.show()
    sys.exit(app.exec())
        