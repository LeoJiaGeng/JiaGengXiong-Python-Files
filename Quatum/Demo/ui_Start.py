# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:53:27 2022

@author: 41137
"""

import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication, QDir
from ui_Quatum import Ui_Form

class QmyWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Quantum")
        self.setAcceptDrops(True)
        self.ui.save_plainTextEdit.setAcceptDrops(False)
        self.ui.search_plainTextEdit.setAcceptDrops(False)

    def MsgWarning(self, msg):
        dlgTitle = "Warning消息框"
        QMessageBox.warning(self, dlgTitle, msg)

    def save_content_show(self, strCont):
        self.ui.save_plainTextEdit.appendPlainText(strCont)

    def search_content_show(self, strCont):
        self.ui.search_plainTextEdit.appendPlainText(strCont)

    def on_btn_clear_clicked(self):
        self.ui.search_plainTextEdit.clear()

    @property
    def content_show(self):
        return self.ui.content_show
    
    @content_show.setter
    def content_show(self, value):
        self.ui.content_show = value

    @pyqtSlot()
    def on_btn_save_energy_clicked(self):
        print("parent class")
        pass

    @pyqtSlot()
    def on_btn_save_freq_clicked(self):
        print("parent class")
        pass

    @pyqtSlot()
    def on_btn_save_coord_clicked(self):
        print("parent class")
        pass    

    def MsgWarning(self, msg):
        dlgTitle = "Warning消息框"
        QMessageBox.warning(self, dlgTitle, msg)

    def dragEnterEvent(self, event) -> None:
        if (event.mimeData().hasUrls()):
            filename = event.mimeData().urls()[0].fileName()
            basename,ext = os.path.splitext(filename)
            ext = ext.upper()
            if (ext == ".LOG"):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        filename = event.mimeData().urls()[0].path()
        cnt = len(filename)
        realname = filename[1:cnt]
        self.ui.edit_file.setText(realname)
        event.accept()
if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyWidget()
    myWidget.show()
    sys.exit(app.exec())
        