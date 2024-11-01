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

    def trans_origin_content_show(self, strCont):
        self.ui.plainTextEdit_trans_origin.appendPlainText(strCont)

    def trans_origin_content_clear(self):
        self.ui.plainTextEdit_trans_origin.clear()

    def trans_new_content_show(self, strCont):
        self.ui.plainTextEdit_trans_new.appendPlainText(strCont)

    def save_content_clear(self):
        self.ui.save_plainTextEdit.clear()

    def table_content_clear(self):
        self.ui.tableInfo.clearContents()

    def search_content_clear(self):
        self.ui.search_plainTextEdit.clear()

    def trans_log_show(self, strCont):
        self.ui.plainTextEdit_trans_log.appendPlainText(strCont)

    @property
    def content_show(self):
        return self.ui.content_show
    
    @content_show.setter
    def content_show(self, value):
        self.ui.content_show = value 

    def open_folder(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择一个目录"
        selectedDir = QFileDialog.getExistingDirectory(self, dlgTitle, curPath, QFileDialog.ShowDirsOnly)
        return selectedDir

    def open_file(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择一个文件"
        filt = "所有文件(*.*);;文本文件(*.txt);;图片文件(*.jpg *.gif *.png)"
        return QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)

    def dragEnterEvent(self, event) -> None:
        if (event.mimeData().hasUrls()):
            filename = event.mimeData().urls()[0].fileName()
            basename,ext = os.path.splitext(filename)
            ext = ext.upper()
            if (ext == ".LOG" or ext == ".GJF" ):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        filename = event.mimeData().urls()[0].path()
        cnt = len(filename)
        realname = filename[1:cnt]
        if self.ui.chebox_trans_sfile.isChecked():
            self.ui.edit_trans_filename.setText(realname)
        else:
            self.ui.edit_file.setText(realname)
        event.accept()

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

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWidget = QmyWidget()
    myWidget.show()
    sys.exit(app.exec())
        