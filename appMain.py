# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: 41137
"""

import sys
sys.path.append(r"D:\Document\Python_Files\Project\Public")
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt, QDir, QThread, pyqtSignal
from ui_Start import QmyWidget
from Files import ReFilenames, SaveFile
from Decoration import Decorator

class QmyApp(QmyWidget):
    def __init__(self):
        super().__init__()
        self.saveFlag = False

    @pyqtSlot()
    def on_btn_search_clicked(self):
        suffix = self.ui.edit_suffix.text()
        file_name = self.ui.edit_filename.text()
        checked = self.ui.check_onlyname.isChecked()

        if (suffix == "" or file_name == ""):
            self.MsgWarning()
        else:
            self.new_line = TestMultiple(suffix, file_name, self.saveFlag, checked)
            self.new_line.sinOut_content.connect(self.on_content_show)
            self.new_line.sinOut_normal_end.connect(self.on_normal_msginfo)
            self.new_line.sinOut_progressBar.connect(self.on_set_progressBar)
            self.new_line.sinOut_progressBar_fullValue.connect(self.on_set_progressBar_fullRange)
            self.new_line.start()
    
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

    @pyqtSlot()
    def on_normal_msginfo(self):
        self.MsgInformation()   

    @pyqtSlot(int)
    def on_set_progressBar(self, value):
        self.ui.progressBar.setValue(value)

    @pyqtSlot(int)
    def on_set_progressBar_fullRange(self, value):
        self.ui.progressBar.setMaximum(value)

class TestMultiple(QThread):
    sinOut_content = pyqtSignal(str)  
    sinOut_normal_end = pyqtSignal() 
    sinOut_progressBar = pyqtSignal(int)
    sinOut_progressBar_fullValue = pyqtSignal(int)  

    def __init__(self, suffix, filename, saveFlag, checked):
        super().__init__()
        self.filename = filename
        self.suffix = suffix
        self.saveFlag = saveFlag
        self.checked = checked

    @Decorator.exe_time("该线程运行时间")
    def run(self):
        self.getname_list = []
        File_names = ReFilenames(self.suffix)
        file_add = str(self.filename)

        self.getname_list = File_names.get_all_files(file_add, self.checked)

        self.sinOut_progressBar_fullValue.emit(len(self.getname_list)-1)
        for index in range(len(self.getname_list)):
            QThread.msleep(1) 
            self.sinOut_content.emit(str(self.getname_list[index]))
            self.sinOut_progressBar.emit(index)
        if self.saveFlag:
            save_obj = SaveFile()
            save_obj.save("save.txt", self.getname_list)

        self.sinOut_normal_end.emit()


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyApp()
    myWidget.show()
    sys.exit(app.exec())
        