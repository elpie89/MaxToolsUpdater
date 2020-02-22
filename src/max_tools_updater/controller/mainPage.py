from PySide2.QtWidgets import QWidget, QVBoxLayout, QMenuBar, QAction, QTabWidget, QLabel, QPushButton,QMainWindow
from PySide2.QtCore import SIGNAL, SLOT
from PySide2.QtCore import Qt
from settingsPage import SettingsPage
from model import configuration
import packageTabView as ptw
reload(ptw)
import logging
import MaxPlus


class MainPage(QMainWindow):

    activePackageWidgets = None
    def __init__(self):
        QMainWindow.__init__(self,MaxPlus.GetQMaxMainWindow())
        self.resize(800, 600)
        self.setWindowTitle("Max Tools Updater")
        self.mainWidget = QWidget(self)
        self.central_layout = QVBoxLayout()
        menu_bar = QMenuBar()
        settingAct = QAction("&Settings", self)
        settingAct.setStatusTip("Open setting window")
        settingAct.connect(SIGNAL("triggered()"), self, SLOT("open()"))
        menu_bar.addAction(settingAct)
        self.mainWidget.setLayout(self.central_layout)
        self.central_layout.addWidget(menu_bar)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.mainWidget)
        self.activePackageWidgets = list()

    def show(self, bringOnTop=None):
        self.loadPackagesTab()
        if bringOnTop:
            self.bringPackageOnTop(bringOnTop)
        QMainWindow.show(self)

    def closeEvent(self,event):
        for packageWidget in self.activePackageWidgets:
            packageWidget.closeQWebEngine()

    def open(self):
        self.settings_window = SettingsPage()
        self.settings_window.show()

    def loadPackagesTab(self):
        for i in range(self.tabs.count()):
            self.tabs.widget(i)
            self.tabs.removeTab(i)

        packagesConfigurationList = configuration.PackageConfiguration.readUserPackages()
        if not packagesConfigurationList:
            self.togglePackagesFoundDialog(True)
        else:
            self.togglePackagesFoundDialog(False)
            self.central_layout.addWidget(self.tabs)
            for i in range(len(packagesConfigurationList)):
                packageConfig = packagesConfigurationList[i]
                package_page = ptw.PackageTabView(packageConfig)
                self.activePackageWidgets.append(package_page)
                if package_page.isValid:
                    self.tabs.addTab(package_page, packageConfig.package_name)
                else:
                    logging.info("package" + packageConfig.package_name + "is not valid")


    def bringPackageOnTop(self, packageConfig):
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if tab.packageConfig.package_name == packageConfig.package_name:
                self.tabs.setCurrentWidget(tab)

    def togglePackagesFoundDialog(self, enabled):
        if enabled:
            no_packages_lbl = QLabel("Ops...No packages found, please add a package from Settings Menu", self)
            no_packages_lbl.setAlignment(Qt.AlignHCenter)
            self.central_layout.addWidget(no_packages_lbl)
            no_packages_lbl.setObjectName("No_Package")
        else:
            no_packages_lbl = self.central_layout.findChild(QLabel, "No_Package")
            self.central_layout.removeWidget(no_packages_lbl)
