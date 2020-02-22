# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Repository\max_tool_updater\src\resources\ui\package_view.ui',
# licensing of 'E:\Repository\max_tool_updater\src\resources\ui\package_view.ui' applies.
#
# Created: Wed Jan 29 01:07:10 2020
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_main_area(object):
    def setupUi(self, main_area):
        main_area.setObjectName("main_area")
        main_area.setEnabled(True)
        main_area.resize(818, 1182)
        main_area.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout = QtWidgets.QVBoxLayout(main_area)
        self.verticalLayout.setObjectName("verticalLayout")
        self.imageLbl = QtWidgets.QLabel(main_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLbl.sizePolicy().hasHeightForWidth())
        self.imageLbl.setSizePolicy(sizePolicy)
        self.imageLbl.setMinimumSize(QtCore.QSize(800, 0))
        self.imageLbl.setMaximumSize(QtCore.QSize(3000, 400))
        self.imageLbl.setText("")
        self.imageLbl.setScaledContents(True)
        self.imageLbl.setWordWrap(False)
        self.imageLbl.setObjectName("imageLbl")
        self.verticalLayout.addWidget(self.imageLbl)
        self.updateArea = QtWidgets.QWidget(main_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.updateArea.sizePolicy().hasHeightForWidth())
        self.updateArea.setSizePolicy(sizePolicy)
        self.updateArea.setMaximumSize(QtCore.QSize(16777215, 50))
        self.updateArea.setObjectName("updateArea")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.updateArea)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.updateLabel = QtWidgets.QLabel(self.updateArea)
        self.updateLabel.setObjectName("updateLabel")
        self.horizontalLayout_2.addWidget(self.updateLabel)
        self.updateBtn = QtWidgets.QPushButton(self.updateArea)
        self.updateBtn.setObjectName("updateBtn")
        self.horizontalLayout_2.addWidget(self.updateBtn)
        self.verticalLayout.addWidget(self.updateArea)
        self.changelogHook = QtWidgets.QWidget(main_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.changelogHook.sizePolicy().hasHeightForWidth())
        self.changelogHook.setSizePolicy(sizePolicy)
        self.changelogHook.setObjectName("changelogHook")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.changelogHook)
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout.addWidget(self.changelogHook)

        self.retranslateUi(main_area)
        QtCore.QMetaObject.connectSlotsByName(main_area)

    def retranslateUi(self, main_area):
        main_area.setWindowTitle(QtWidgets.QApplication.translate("main_area", "Form", None, -1))
        self.updateLabel.setText(QtWidgets.QApplication.translate("main_area", "TextLabel", None, -1))
        self.updateBtn.setText(QtWidgets.QApplication.translate("main_area", "Update", None, -1))

