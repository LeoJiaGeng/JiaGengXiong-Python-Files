# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: 41137
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication, QDir
from ui_Search import Ui_Form

class QmyWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("firmware")

    @property
    def filename(self):
        return self.ui.edit_filename
    
    @filename.setter
    def filename(self, value):
        self.ui.edit_filename = value

    @property
    def suffix(self):
        return self.ui.edit_suffix
    
    @suffix.setter
    def suffix(self, value):
        self.ui.edit_suffix = value

    @property
    def content_show(self):
        return self.ui.content_show
    
    @content_show.setter
    def content_show(self, value):
        self.ui.content_show = value

    def on_btn_search_clicked(self):
        print("父函数")
        pass

    def on_btn_clear_clicked(self):
        print("父函数")
        pass    

    def on_check_onlyname_clicked(self):
        print("父函数")
        pass

    @pyqtSlot()
    def MsgWarning(self, strInfo):
        dlgTitle = "Warning消息框"
        QMessageBox.warning(self, dlgTitle, strInfo)

    @pyqtSlot()
    def MsgInformation(self):
        dlgTitle = "Information消息框"
        strInfo = "文件已搜索完成！"
        QMessageBox.information(self, dlgTitle, strInfo)
        
if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyWidget()
    myWidget.show()
    sys.exit(app.exec())
        