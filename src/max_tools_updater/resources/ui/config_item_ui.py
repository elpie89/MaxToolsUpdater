# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Repository\max_tool_updater\src\resources\ui\config_item.ui',
# licensing of 'E:\Repository\max_tool_updater\src\resources\ui\config_item.ui' applies.
#
# Created: Wed Jan 29 01:07:10 2020
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PackageConfiguration(object):
    def setupUi(self, PackageConfiguration):
        PackageConfiguration.setObjectName("PackageConfiguration")
        PackageConfiguration.resize(646, 360)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PackageConfiguration.sizePolicy().hasHeightForWidth())
        PackageConfiguration.setSizePolicy(sizePolicy)
        PackageConfiguration.setMinimumSize(QtCore.QSize(400, 110))
        PackageConfiguration.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout_3 = QtWidgets.QGridLayout(PackageConfiguration)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.vcs_widget = QtWidgets.QWidget(PackageConfiguration)
        self.vcs_widget.setObjectName("vcs_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.vcs_widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.client_lbl = QtWidgets.QLabel(self.vcs_widget)
        self.client_lbl.setObjectName("client_lbl")
        self.gridLayout_2.addWidget(self.client_lbl, 1, 0, 1, 1)
        self.client_edit = QtWidgets.QLineEdit(self.vcs_widget)
        self.client_edit.setObjectName("client_edit")
        self.gridLayout_2.addWidget(self.client_edit, 1, 1, 1, 1)
        self.vcs_combobox = QtWidgets.QComboBox(self.vcs_widget)
        self.vcs_combobox.setObjectName("vcs_combobox")
        self.vcs_combobox.addItem("")
        self.gridLayout_2.addWidget(self.vcs_combobox, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.vcs_widget, 8, 0, 2, 3)
        self.packageNameLbl = QtWidgets.QLabel(PackageConfiguration)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setUnderline(True)
        font.setBold(True)
        self.packageNameLbl.setFont(font)
        self.packageNameLbl.setObjectName("packageNameLbl")
        self.gridLayout_3.addWidget(self.packageNameLbl, 0, 0, 1, 2)
        self.connectionType = QtWidgets.QComboBox(PackageConfiguration)
        self.connectionType.setObjectName("connectionType")
        self.connectionType.addItem("")
        self.connectionType.addItem("")
        self.gridLayout_3.addWidget(self.connectionType, 1, 0, 1, 1)
        self.packageName = QtWidgets.QLineEdit(PackageConfiguration)
        self.packageName.setObjectName("packageName")
        self.gridLayout_3.addWidget(self.packageName, 0, 2, 1, 1)
        self.networkPath = QtWidgets.QLineEdit(PackageConfiguration)
        self.networkPath.setObjectName("networkPath")
        self.gridLayout_3.addWidget(self.networkPath, 2, 2, 1, 1)
        self.hostLbl = QtWidgets.QLabel(PackageConfiguration)
        self.hostLbl.setObjectName("hostLbl")
        self.gridLayout_3.addWidget(self.hostLbl, 3, 0, 1, 1)
        self.pathLbl = QtWidgets.QLabel(PackageConfiguration)
        self.pathLbl.setObjectName("pathLbl")
        self.gridLayout_3.addWidget(self.pathLbl, 2, 0, 1, 1)
        self.passwordLbl = QtWidgets.QLabel(PackageConfiguration)
        self.passwordLbl.setObjectName("passwordLbl")
        self.gridLayout_3.addWidget(self.passwordLbl, 5, 0, 1, 1)
        self.ftpPathLbl = QtWidgets.QLabel(PackageConfiguration)
        self.ftpPathLbl.setObjectName("ftpPathLbl")
        self.gridLayout_3.addWidget(self.ftpPathLbl, 6, 0, 1, 1)
        self.password = QtWidgets.QLineEdit(PackageConfiguration)
        self.password.setObjectName("password")
        self.gridLayout_3.addWidget(self.password, 5, 2, 1, 1)
        self.host = QtWidgets.QLineEdit(PackageConfiguration)
        self.host.setObjectName("host")
        self.gridLayout_3.addWidget(self.host, 3, 2, 1, 1)
        self.username = QtWidgets.QLineEdit(PackageConfiguration)
        self.username.setObjectName("username")
        self.gridLayout_3.addWidget(self.username, 4, 2, 1, 1)
        self.usernameLbl = QtWidgets.QLabel(PackageConfiguration)
        self.usernameLbl.setObjectName("usernameLbl")
        self.gridLayout_3.addWidget(self.usernameLbl, 4, 0, 1, 1)
        self.ftppath = QtWidgets.QLineEdit(PackageConfiguration)
        self.ftppath.setObjectName("ftppath")
        self.gridLayout_3.addWidget(self.ftppath, 6, 2, 1, 1)
        self.vcs_checkbox = QtWidgets.QCheckBox(PackageConfiguration)
        self.vcs_checkbox.setObjectName("vcs_checkbox")
        self.gridLayout_3.addWidget(self.vcs_checkbox, 7, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 10, 2, 1, 1)

        self.retranslateUi(PackageConfiguration)
        QtCore.QMetaObject.connectSlotsByName(PackageConfiguration)

    def retranslateUi(self, PackageConfiguration):
        PackageConfiguration.setWindowTitle(QtWidgets.QApplication.translate("PackageConfiguration", "PackageConfiguration", None, -1))
        self.client_lbl.setText(QtWidgets.QApplication.translate("PackageConfiguration", "Client", None, -1))
        self.vcs_combobox.setItemText(0, QtWidgets.QApplication.translate("PackageConfiguration", "Perforce", None, -1))
        self.packageNameLbl.setText(QtWidgets.QApplication.translate("PackageConfiguration", "Package Name", None, -1))
        self.connectionType.setItemText(0, QtWidgets.QApplication.translate("PackageConfiguration", "Local", None, -1))
        self.connectionType.setItemText(1, QtWidgets.QApplication.translate("PackageConfiguration", "FTP", None, -1))
        self.hostLbl.setText(QtWidgets.QApplication.translate("PackageConfiguration", "Host", None, -1))
        self.pathLbl.setText(QtWidgets.QApplication.translate("PackageConfiguration", "Package path", None, -1))
        self.passwordLbl.setText(QtWidgets.QApplication.translate("PackageConfiguration", "Password", None, -1))
        self.ftpPathLbl.setText(QtWidgets.QApplication.translate("PackageConfiguration", "FTPPath", None, -1))
        self.usernameLbl.setText(QtWidgets.QApplication.translate("PackageConfiguration", "Username", None, -1))
        self.vcs_checkbox.setText(QtWidgets.QApplication.translate("PackageConfiguration", "VCS Integration", None, -1))

