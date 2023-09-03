# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: 41137
"""

import sys

from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt, QDir
from ui_Start import QmyWidget

from sort_file import SortFiles
from config_adapt import Config_Adapt

class QmyApp(QmyWidget):
    def __init__(self):
        super().__init__()
        self.init()
        self.convert = SortFiles()
        
    def init(self):
        self.config_init() # Initialize config file
        self.params_init() # Initialize params file
        self.connecter_init() # Initialize signals and slots

    def config_init(self):
        self.config = Config_Adapt("config.ini")
        self.ui.line_edit_files.setText(self.config.get_config("input", "file_name")["data"])
        self.ui.line_edit_num.setText(self.config.get_config("input", "num")["data"])

    def params_init(self):
        self.read_type = 0
        self.write_type = 0
        self.suffix = 'xls'

    def connecter_init(self):
        self.ui.radio_btn_read_col.clicked.connect(self.do_set_read_type)
        self.ui.radio_btn_read_row.clicked.connect(self.do_set_read_type)

        self.ui.radio_btn_write_col.clicked.connect(self.do_set_write_type)
        self.ui.radio_btn_write_row.clicked.connect(self.do_set_write_type)

    @pyqtSlot(str)
    def on_comboBox_currentIndexChanged(self, curText):
        self.suffix = curText

    @pyqtSlot()
    def on_btn_open_files_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择一个目录"
        selectedDir = QFileDialog.getExistingDirectory(self, dlgTitle, curPath, QFileDialog.ShowDirsOnly)
        self.ui.line_edit_files.setText(selectedDir)

    def do_set_read_type(self):
        if (self.ui.radio_btn_read_col.isChecked()):
            self.read_type = 0
        elif (self.ui.radio_btn_read_row.isChecked()):
            self.read_type = 1

    def do_set_write_type(self):
        if (self.ui.radio_btn_write_col.isChecked()):
            self.write_type = 0
        elif (self.ui.radio_btn_write_row.isChecked()):
            self.write_type = 1

    @pyqtSlot()
    def on_btn_convert_clicked(self):
        self.ui.plainTextEdit.appendPlainText("正在统计... ...")

        file_name = self.ui.line_edit_files.text()
        num_list = [int(self.ui.line_edit_num.text())]
        self.convert.main_function(self.suffix, file_name, num_list, self.read_type, self.write_type)

        self.ui.plainTextEdit.appendPlainText("统计完成！")

    @pyqtSlot()
    def on_btn_csv_xlsx_clicked(self):
        self.ui.plainTextEdit.appendPlainText("正在转换... ...")
        
        file_name = self.ui.line_edit_files.text()
        self.convert.main_convert(file_name)

        self.ui.plainTextEdit.appendPlainText("转换完成！")

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyApp()
    myWidget.show()
    sys.exit(app.exec())
        