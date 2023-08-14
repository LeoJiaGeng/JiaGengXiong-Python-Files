# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Document\Python_Files\Project\Gui\Tools\..\Demo\Search.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 595)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.edit_filename = QtWidgets.QLineEdit(self.groupBox)
        self.edit_filename.setObjectName("edit_filename")
        self.horizontalLayout.addWidget(self.edit_filename)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 8)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edit_suffix = QtWidgets.QLineEdit(self.groupBox)
        self.edit_suffix.setObjectName("edit_suffix")
        self.horizontalLayout_2.addWidget(self.edit_suffix)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.check_onlyname = QtWidgets.QCheckBox(self.groupBox)
        self.check_onlyname.setObjectName("check_onlyname")
        self.horizontalLayout_2.addWidget(self.check_onlyname)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 6)
        self.horizontalLayout_2.setStretch(4, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_search = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout_3.addWidget(self.btn_search)
        self.btn_clear = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_clear.setObjectName("btn_clear")
        self.horizontalLayout_3.addWidget(self.btn_clear)
        self.btn_saveLog = QtWidgets.QPushButton(self.groupBox_3)
        icon = QtGui.QIcon.fromTheme("bold")
        self.btn_saveLog.setIcon(icon)
        self.btn_saveLog.setCheckable(True)
        self.btn_saveLog.setChecked(False)
        self.btn_saveLog.setAutoExclusive(True)
        self.btn_saveLog.setObjectName("btn_saveLog")
        self.horizontalLayout_3.addWidget(self.btn_saveLog)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.content_show = QtWidgets.QTextBrowser(self.groupBox_2)
        self.content_show.setObjectName("content_show")
        self.verticalLayout_3.addWidget(self.content_show)
        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "输入区"))
        self.label.setText(_translate("Form", "文件夹："))
        self.pushButton.setText(_translate("Form", "选择文件夹"))
        self.label_2.setText(_translate("Form", "后缀名："))
        self.label_3.setText(_translate("Form", "进度："))
        self.check_onlyname.setText(_translate("Form", "仅输出文件名"))
        self.groupBox_3.setTitle(_translate("Form", "功能按钮"))
        self.btn_search.setText(_translate("Form", "搜索"))
        self.btn_clear.setText(_translate("Form", "清空"))
        self.btn_saveLog.setText(_translate("Form", "存日志"))
        self.groupBox_2.setTitle(_translate("Form", "输出区"))
