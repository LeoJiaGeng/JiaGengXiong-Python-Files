# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: 41137
"""

import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt, QDir, QThread, pyqtSignal
from ui_Start import QmyWidget

from Public.files import ReFilenames, SaveFile
from Public.decoration import Decorator
from config_adapt import Config_Adapt
from Public.common import *

class QmyApp(QmyWidget):
    def __init__(self):
        super().__init__()
        self.saveFlag = False
        self.content_show_flag = True
        self.config_init()

    def config_init(self):
        self.config = Config_Adapt("config.ini")
        self.ui.edit_filename.setText(self.config.get_config("input", "file_name")["data"])
        self.ui.edit_suffix.setText(self.config.get_config("input", "suffix")["data"])
        self.ui.edit_re_search.setText(self.config.get_config("input", "re_search")["data"])

    @pyqtSlot()
    def on_btn_search_clicked(self):
        suffix = self.ui.edit_suffix.text()
        file_name = self.ui.edit_filename.text()
        checked = self.ui.check_onlyname.isChecked()

        if check_or_none(suffix, file_name):
            self.MsgWarning("请同时输入文件夹和后缀名")
        else:
            self.new_line = TestMultiple(suffix, file_name, self.saveFlag, checked)
            self.new_line.sinOut_content_progressBar[int].connect(self.on_set_progressBar)
            self.new_line.sinOut_content_progressBar[str].connect(self.on_content_show)

            self.new_line.sinOut_Bar_fullValue_msg.connect(self.on_normal_msginfo)
            self.new_line.sinOut_Bar_fullValue_msg[int].connect(self.on_set_progressBar_fullRange)
            self.new_line.start()
        
        self.config.set_config("input", "suffix", suffix)
        self.config.set_config("input", "file_name", file_name)
    
    @pyqtSlot()
    def on_btn_clear_clicked(self):
        self.ui.content_show.clear()

    @pyqtSlot(bool)
    def on_btn_saveLog_clicked(self, checked):
        if checked:
            self.saveFlag = True
        else:
            self.saveFlag = False

    @pyqtSlot()
    def on_pushButton_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择一个目录"
        selectedDir = QFileDialog.getExistingDirectory(self, dlgTitle, curPath, QFileDialog.ShowDirsOnly)
        self.ui.edit_filename.setText(selectedDir)

    @pyqtSlot(str)
    def on_content_show(self, strCont):
        self.ui.content_show.append(strCont)

    @pyqtSlot(int)
    def on_set_progressBar(self, value):
        self.ui.progressBar.setValue(value)

    @pyqtSlot()
    def on_normal_msginfo(self):
        self.MsgInformation()  

    @pyqtSlot(int)
    def on_set_progressBar_fullRange(self, value):
        self.ui.progressBar.setMaximum(value)

    @pyqtSlot()
    def on_content_show_textChanged(self):
        self.content_show_flag = False
        
    @pyqtSlot()
    def on_btn_re_search_clicked(self):
        """move mouse cursor to re_search result"""
        filter_content = self.ui.edit_re_search.text()
        all_str = self.ui.content_show.toPlainText()
        all_list = list(all_str.split('\n'))
        self.content_show_flag = True

        for content in all_list:
            if filter_content in content:
                self.on_content_show("\n" + content)
        # 
        if self.content_show_flag:
            self.on_content_show("\n没有搜索到指定的内容！")
        self.config.set_config("input", "re_search", filter_content)

class TestMultiple(QThread):
    sinOut_content_progressBar = pyqtSignal([str], [int])  
    sinOut_Bar_fullValue_msg = pyqtSignal([], [int])   

    def __init__(self, suffix, filename, saveFlag, checked):
        super().__init__()
        self.filename = filename
        self.suffix = suffix
        self.saveFlag = saveFlag
        self.checked = checked

    @Decorator.exe_time("该线程运行时间:")
    def run(self):
        self.getname_list = []
        File_names = ReFilenames(self.suffix)
        file_add = str(self.filename)

        self.getname_list = File_names.get_all_files(file_add, self.checked)
        print(f"含有该后缀名的文件个数为：{len(File_names)}")
        self.sinOut_Bar_fullValue_msg[int].emit(len(self.getname_list)-1)

        if (len(self.getname_list) != 0):
            for index in range(len(self.getname_list)):
                self.sinOut_content_progressBar[str].emit(str(self.getname_list[index]))
                self.sinOut_content_progressBar[int].emit(index)
            if self.saveFlag:
                save_obj = SaveFile()
                save_obj.save("save.txt", self.getname_list)

            self.sinOut_Bar_fullValue_msg.emit()
        else:
            self.sinOut_content_progressBar[str].emit("未匹配到该文件后缀名！")

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyApp()
    myWidget.show()
    sys.exit(app.exec())
        