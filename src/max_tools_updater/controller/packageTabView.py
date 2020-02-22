from PySide2 import QtUiTools
from PySide2.QtWidgets import *
from PySide2 import QtWebEngineWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWebChannel import QWebChannel
import os
import qtUtility
import utility
import logging

from model.configuration import VCSType, PackageConfiguration
from vcs import p4manager
from vcs.vcsManager import *
from resources.ui import package_view_ui
from setup.installer import Installer
import subprocess

class PackageTabView(QWidget, package_view_ui.Ui_main_area):

    def __init__(self, packageConfig):
        super(PackageTabView, self).__init__()
        self.setupUi(self)
        self.packageConfig = packageConfig

        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

        self.updateBtn.clicked.connect(self.onUpdateBtnClicked)

        self.changelog_layout = QVBoxLayout()
        self.changelogHook.setLayout(self.changelog_layout)

        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.changelogHook)
        self.page = self.webEngineView.page()
        self.app_manager = AppManager(self.packageConfig)
        channel = QWebChannel(self)
        self.page.setWebChannel(channel)
        channel.registerObject("app_manager", self.app_manager)
        packageFolder = self.packageConfig.getPackageLocation()
        indexPath = packageFolder + "/index.html"
        if os.path.exists(indexPath):
            url = QUrl.fromLocalFile(indexPath)
            self.webEngineView.setUrl(url)
        else:
            self.webEngineView.setContent("Something went wrong during package installation, please reinstall tool package")
        self.changelog_layout.addWidget(self.webEngineView)
        self.webEngineView.setContentsMargins(0, 0, 10, 0)
        self.webEngineView.loadFinished.connect(self.resizeWebView)

        self.resizeEvent = self.onResize
        self.isValid = True


        if self.packageConfig.use_vcs and self.packageConfig.vcs_type == VCSType.Perforce:
            currentVersion = utility.getServerVersion(self.packageConfig)
        else:
            currentVersion = PackageConfiguration.getCurrentVersion2(self.packageConfig)

        if not currentVersion:
            # self.isValid = False
            logging.info("impossible to retrieve server version for package: {0}".format(packageConfig.package_name))
            # return

        userVersion = self.packageConfig.getUserVersion()
        if not userVersion:
            self.isValid = False
            logging.info("impossible to retrieve local version for package: {0}".format(packageConfig.package_name))
            return

        self.display_version_info(userVersion, currentVersion)
        self.showImage()

    def onResize(self, sizeEvent):
        self.webEngineView.resize(sizeEvent.size())

    def resizeWebView(self):
        self.webEngineView.resize(self.size())

    def onUpdateBtnClicked(self):
        if qtUtility.confirmRestart():
            if self.packageConfig.use_vcs and self.packageConfig.vcs_type == VCSType.Perforce:
                p4manager.syncPackage(self.packageConfig)
            installer = Installer()
            installer.updatePackage(userPackage=self.packageConfig)

    def display_version_info(self, local_version, publish_version):
        self.updateLabel.setText(local_version)
        is_updated = utility.isPackageUpdated(local_version, publish_version)
        self.updateBtn.setVisible(not is_updated)

    def showImage(self):
        img = self.packageConfig.getPackageImage()
        main_pixmap = QPixmap(":/images/company_logo.png")
        if os.path.exists(img):
            main_pixmap = QPixmap(img)
        self.imageLbl.setPixmap(main_pixmap)

    def closeQWebEngine(self):
        process = subprocess.Popen('taskkill /IM "QtWebEngineProcess.exe" /F', shell=True)
        process.wait()

class AppManager(QObject):
    textChanged = Signal(str)

    def __init__(self, packageConfig):
        QObject.__init__(self)
        self.m_text = ""
        self.packageConfig = packageConfig
        timer = QTimer(self)
        timer.singleShot(1000, self.on_timeout)

    def on_timeout(self):
        self.text = QDateTime.currentDateTime().toString()

    @Property(str, notify=textChanged)
    def text(self):
        return self.m_text

    @text.setter
    def setText(self, text):
        if self.m_text == text:
            return
        file_path = self.packageConfig.getMarkDown()
        markdown_file = open(file_path, "r")
        file_content = markdown_file.read()
        self.m_text = file_content
        self.textChanged.emit(self.m_text)
