# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: 41137
"""

import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt, QDir, QThread, pyqtSignal
from ui_Start import QmyWidget
from quantum import Quantum
from Public.config import Config

class QmyApp(QmyWidget):
    def __init__(self):
        super().__init__()
        self.config_init()

    def config_init(self):
        self.config = Config("quatum_config.ini")
        self.ui.edit_files.setText(self.config.get_config("save", "file_name")["data"])
        self.ui.edit_file.setText(self.config.get_config("search", "file_name")["data"])

    def save_edit_files_config(self, content):
        """Save the contents of the line edit in saving window"""
        self.config.set_config("save", "file_name", content)    

    def save_edit_file_config(self, content):
        """Save the contents of the line edit in searching window"""
        self.config.set_config("search", "file_name", content)

    @pyqtSlot()
    def on_btn_open_files_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择一个目录"
        selectedDir = QFileDialog.getExistingDirectory(self, dlgTitle, curPath, QFileDialog.ShowDirsOnly)
        self.ui.edit_files.setText(selectedDir)
        self.save_edit_files_config(selectedDir)

    @pyqtSlot()
    def on_btn_open_file_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择一个文件"
        filt = "所有文件(*.*);;文本文件(*.txt);;图片文件(*.jpg *.gif *.png)"
        fileList, filt = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        self.ui.edit_file.setText(fileList)
        self.save_edit_file_config(fileList)

    @pyqtSlot()
    def on_btn_save_energy_clicked(self):
        self.save_content_show("Saving energy... ...")
        file_name = self.ui.edit_files.text()
        self.quant = Quantum("log",file_name)
        self.quant.save_energy()
        self.save_content_show("Save OK!")
        self.save_edit_files_config(file_name)

    @pyqtSlot()
    def on_btn_save_freq_clicked(self):
        self.save_content_show("Saving frequency... ...")
        file_name = self.ui.edit_files.text()
        self.quant = Quantum("log",file_name)
        self.quant.save_freq()
        self.save_content_show("Save OK!")
        self.save_edit_files_config(file_name)

    @pyqtSlot()
    def on_btn_save_coord_clicked(self):
        self.save_content_show("Saving coordinates... ...")
        file_name = self.ui.edit_files.text()
        self.quant = Quantum("log",file_name)
        self.quant.save_cor()
        self.save_content_show("Save OK!")
        self.save_edit_files_config(file_name)

    @pyqtSlot()
    def on_btn_find_ver_clicked(self):
        self.search_content_show("Searching eigenvectors... ...")
        file_name = self.ui.edit_file.text()
        self.quant = Quantum("log",file_name)

        for content in self.quant.print_eigenvectors():
            self.search_content_show(content)
        self.search_content_show("Search OK!")
        self.save_edit_file_config(file_name)

    @pyqtSlot()
    def on_btn_find_yes_clicked(self):
        self.search_content_show("Searching eigenvectors... ...")
        file_name = self.ui.edit_file.text()
        self.quant = Quantum("log",file_name)

        for content in self.quant.print_eigenvectors_YES():
            self.search_content_show(content)
        self.search_content_show("Search OK!")
        self.save_edit_file_config(file_name)

class QuaThread(QThread):
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
        