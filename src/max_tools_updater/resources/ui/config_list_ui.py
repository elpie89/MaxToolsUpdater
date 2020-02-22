# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Repository\max_tool_updater\src\resources\ui\config_list.ui',
# licensing of 'E:\Repository\max_tool_updater\src\resources\ui\config_list.ui' applies.
#
# Created: Wed Jan 29 01:07:10 2020
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_main_area(object):
    def setupUi(self, main_area):
        main_area.setObjectName("main_area")
        main_area.setWindowModality(QtCore.Qt.ApplicationModal)
        main_area.resize(782, 600)
        main_area.setMinimumSize(QtCore.QSize(600, 600))
        main_area.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.horizontalLayout = QtWidgets.QHBoxLayout(main_area)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(main_area)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addPackage = QtWidgets.QPushButton(main_area)
        self.addPackage.setObjectName("addPackage")
        self.verticalLayout.addWidget(self.addPackage)
        self.removePackage = QtWidgets.QPushButton(main_area)
        self.removePackage.setObjectName("removePackage")
        self.verticalLayout.addWidget(self.removePackage)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.logInstructions = QtWidgets.QCheckBox(main_area)
        self.logInstructions.setObjectName("logInstructions")
        self.verticalLayout.addWidget(self.logInstructions)
        self.saveBtn = QtWidgets.QPushButton(main_area)
        self.saveBtn.setObjectName("saveBtn")
        self.verticalLayout.addWidget(self.saveBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(main_area)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(main_area)

    def retranslateUi(self, main_area):
        main_area.setWindowTitle(QtWidgets.QApplication.translate("main_area", "Settings", None, -1))
        self.addPackage.setText(QtWidgets.QApplication.translate("main_area", "Add Package", None, -1))
        self.removePackage.setText(QtWidgets.QApplication.translate("main_area", "Remove Package", None, -1))
        self.logInstructions.setText(QtWidgets.QApplication.translate("main_area", "Log Intructions", None, -1))
        self.saveBtn.setText(QtWidgets.QApplication.translate("main_area", "Apply", None, -1))

