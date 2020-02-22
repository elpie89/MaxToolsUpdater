from PySide2.QtWidgets import QListWidgetItem, QMainWindow, QWidget
from PySide2.QtCore import Signal
from model import configuration
from configurationItemView import ConfigurationItemView
from model.configuration import VCSType
from setup.installer import Installer
from resources.ui import config_list_ui
import controller.qtUtility as QtUtility
import vcs.p4manager as p4manager


class SettingsPage(QWidget, config_list_ui.Ui_main_area):
    settingChanged = Signal()

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.addPackage.clicked.connect(self.onAddUserPackageClicked)
        self.removePackage.clicked.connect(self.onRemoveUserPackageClicked)
        self.saveBtn.clicked.connect(self.onApplyBtnClicked)

        self.packagesConfigurationList = configuration.PackageConfiguration.readUserPackages()
        if self.packagesConfigurationList:
            for packagesConfig in self.packagesConfigurationList:
                self.onAddUserPackageClicked(content=packagesConfig)

    def onAddUserPackageClicked(self, content=None):
        ''' add empty item in the ui'''
        package_setting_widget = ConfigurationItemView(content)
        tabname = "Package"
        if content:
            tabname = content.package_name
        self.tabWidget.addTab(package_setting_widget, tabname)

    def onRemoveUserPackageClicked(self):
        ''' remove the item from the ui and set package to remove in Installer singleton'''
        installer = Installer()
        itemWidget = self.tabWidget.currentWidget()
        self.tabWidget.removeTab(self.tabWidget.currentIndex())
        if itemWidget:
            deletablePackage = itemWidget.get_setting()
            installer.deletePackages.append(deletablePackage)

    def getUserPackagesData(self):
        """pack all settings prompted by user in ui into a list of PackageConfiguration"""
        userPackagesData = list()
        for index in range(self.tabWidget.count()):
            item = self.tabWidget.widget(index)
            package_setting_data = item.get_setting()
            if package_setting_data:
                userPackagesData.append(package_setting_data)
        return userPackagesData

    def onApplyBtnClicked(self):
        # do installation /remove only on installer class
        if QtUtility.confirmRestart():
            currentUserPackages = self.getUserPackagesData()
            configuration.PackageConfiguration.saveUserPackages(currentUserPackages)
            self.settingChanged.emit()
            userPackages = configuration.PackageConfiguration.readUserPackages()
            for package in userPackages:
                if package.use_vcs and package.vcs_type == VCSType.Perforce:
                    p4manager.syncPackage(package)
            installer = Installer()
            installer.userPackages = userPackages
            installer.reinstallPackages(log=self.logInstructions.isChecked())
