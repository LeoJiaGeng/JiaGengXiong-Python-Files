# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Document\Python_Files\Project\Gui\Tools\..\Demo_Guoliang\ui_excel.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(779, 684)
        Form.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.function = QtWidgets.QGroupBox(Form)
        self.function.setStyleSheet("QGroupBox{    \n"
"    background-color: rgb(255, 254, 235);\n"
"    color: rgb(0, 85, 255);\n"
"}")
        self.function.setObjectName("function")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.function)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_open_files = QtWidgets.QPushButton(self.function)
        self.btn_open_files.setObjectName("btn_open_files")
        self.horizontalLayout_3.addWidget(self.btn_open_files)
        self.line_edit_files = QtWidgets.QLineEdit(self.function)
        self.line_edit_files.setObjectName("line_edit_files")
        self.horizontalLayout_3.addWidget(self.line_edit_files)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.function)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.function)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/pictures/icos/DM_20230815124713_039.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ico/pictures/icos/DM_20230815124713_016.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon1, "")
        self.horizontalLayout_6.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.function)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.line_edit_num = QtWidgets.QLineEdit(self.function)
        self.line_edit_num.setMaximumSize(QtCore.QSize(50, 20))
        self.line_edit_num.setObjectName("line_edit_num")
        self.horizontalLayout_6.addWidget(self.line_edit_num)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.btn_head = QtWidgets.QPushButton(self.function)
        self.btn_head.setCheckable(True)
        self.btn_head.setObjectName("btn_head")
        self.horizontalLayout_6.addWidget(self.btn_head)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 2)
        self.horizontalLayout_6.setStretch(3, 1)
        self.horizontalLayout_6.setStretch(4, 1)
        self.horizontalLayout_6.setStretch(5, 2)
        self.horizontalLayout_6.setStretch(6, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.frame_3 = QtWidgets.QFrame(self.function)
        self.frame_3.setStyleSheet("QFrame{    \n"
"\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.frame_2 = QtWidgets.QFrame(self.frame_3)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radio_btn_read_row = QtWidgets.QRadioButton(self.frame_2)
        self.radio_btn_read_row.setChecked(True)
        self.radio_btn_read_row.setObjectName("radio_btn_read_row")
        self.horizontalLayout_2.addWidget(self.radio_btn_read_row)
        self.radio_btn_read_col = QtWidgets.QRadioButton(self.frame_2)
        self.radio_btn_read_col.setObjectName("radio_btn_read_col")
        self.horizontalLayout_2.addWidget(self.radio_btn_read_col)
        self.horizontalLayout_4.addWidget(self.frame_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.frame = QtWidgets.QFrame(self.frame_3)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.radio_btn_write_col = QtWidgets.QRadioButton(self.frame)
        self.radio_btn_write_col.setChecked(True)
        self.radio_btn_write_col.setObjectName("radio_btn_write_col")
        self.horizontalLayout.addWidget(self.radio_btn_write_col)
        self.radio_btn_write_row = QtWidgets.QRadioButton(self.frame)
        self.radio_btn_write_row.setObjectName("radio_btn_write_row")
        self.horizontalLayout.addWidget(self.radio_btn_write_row)
        self.horizontalLayout_4.addWidget(self.frame)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.function)
        self.button = QtWidgets.QGroupBox(Form)
        self.button.setStyleSheet("QGroupBox{    \n"
"    background-color: rgb(255, 254, 235);\n"
"    color: rgb(0, 85, 255);\n"
"}")
        self.button.setObjectName("button")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.button)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.btn_convert = QtWidgets.QPushButton(self.button)
        self.btn_convert.setObjectName("btn_convert")
        self.horizontalLayout_5.addWidget(self.btn_convert)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.btn_csv_xlsx = QtWidgets.QPushButton(self.button)
        self.btn_csv_xlsx.setObjectName("btn_csv_xlsx")
        self.horizontalLayout_5.addWidget(self.btn_csv_xlsx)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addWidget(self.button)
        self.show = QtWidgets.QGroupBox(Form)
        self.show.setStyleSheet("QGroupBox{    \n"
"    background-color: rgb(255, 254, 235);\n"
"    color: rgb(0, 85, 255);\n"
"}")
        self.show.setObjectName("show")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.show)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.show)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_3.addWidget(self.plainTextEdit)
        self.verticalLayout.addWidget(self.show)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 8)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.function.setTitle(_translate("Form", "功能区"))
        self.btn_open_files.setText(_translate("Form", "打开文件夹："))
        self.label_2.setText(_translate("Form", "文件类型:"))
        self.comboBox.setItemText(0, _translate("Form", "xls"))
        self.comboBox.setItemText(1, _translate("Form", "xlsx"))
        self.label.setText(_translate("Form", "提取的行/列数："))
        self.btn_head.setText(_translate("Form", "是否写入表头"))
        self.label_3.setText(_translate("Form", "提取文件的方向"))
        self.radio_btn_read_row.setText(_translate("Form", "提取行"))
        self.radio_btn_read_col.setText(_translate("Form", "提取列"))
        self.label_4.setText(_translate("Form", "写入文件的方向"))
        self.radio_btn_write_col.setText(_translate("Form", "写入行"))
        self.radio_btn_write_row.setText(_translate("Form", "写入列"))
        self.button.setTitle(_translate("Form", "按钮"))
        self.btn_convert.setText(_translate("Form", "提取文件"))
        self.btn_csv_xlsx.setText(_translate("Form", "csv转xlsx"))
        self.show.setTitle(_translate("Form", "显示区"))
import ico_rc
