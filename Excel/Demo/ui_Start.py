# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: 41137
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import  QCoreApplication, Qt, pyqtSlot
from ui_Excel import Ui_Form

class QmyWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Excel 小工具")

    @pyqtSlot()
    def MsgWarning(self, strInfo):
        dlgTitle = "Warning消息框"
        QMessageBox.warning(self, dlgTitle, strInfo)

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyWidget()
    myWidget.show()
    sys.exit(app.exec())
        