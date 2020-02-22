from PySide2.QtWidgets import *

from model import configuration
from resources.ui import config_item_ui
import vcs.p4manager as p4

class ConfigurationItemView(QWidget, config_item_ui.Ui_PackageConfiguration):

    def __init__(self, packageConfig):
        QWidget.__init__(self)
        self.setupUi(self)
        self.connectionType.currentIndexChanged.connect(self.on_index_changed)
        self.vcs_checkbox.stateChanged.connect(self.on_vcs_checkbox_changed)

        self.isValid = False

        if packageConfig:
            self.packageConfiguration = packageConfig
            self.load_setting()
        else:
            self.packageConfiguration = configuration.PackageConfiguration()

        if self.packageConfiguration.connection_type == configuration.ConnectionType.LOCAL:
            self.display_network_ui()
        elif self.packageConfiguration.connection_type == configuration.ConnectionType.FTP:
            self.display_ftp_ui()

        self.vcs_checkbox.setChecked(self.packageConfiguration.use_vcs)
        self.vcs_widget.setEnabled(self.vcs_checkbox.isChecked())

    def on_vcs_checkbox_changed(self):
        self.vcs_widget.setEnabled(self.vcs_checkbox.isChecked())

    def on_index_changed(self, index):
        if index == 0:
            self.display_network_ui()
            self.packageConfiguration.set_local_network_connection()
        if index == 1:
            self.display_ftp_ui()
            self.packageConfiguration.set_ftp_connection()

    def display_ftp_ui(self):
        self.networkPath.setDisabled(True)
        self.networkPath.hide()
        self.pathLbl.hide()
        self.host.setEnabled(True)
        self.host.show()
        self.hostLbl.show()
        self.password.setEnabled(True)
        self.password.show()
        self.passwordLbl.show()
        self.username.setEnabled(True)
        self.username.show()
        self.usernameLbl.show()
        self.ftppath.setEnabled(True)
        self.ftppath.show()
        self.ftpPathLbl.show()

    def display_network_ui(self):
        self.networkPath.setEnabled(True)
        self.networkPath.show()
        self.pathLbl.show()
        self.host.setDisabled(True)
        self.host.hide()
        self.hostLbl.hide()
        self.password.setDisabled(True)
        self.password.hide()
        self.passwordLbl.hide()
        self.username.setDisabled(True)
        self.username.hide()
        self.usernameLbl.hide()
        self.ftppath.setDisabled(True)
        self.ftppath.hide()
        self.ftpPathLbl.hide()

    def load_setting(self):
        self.packageName.setText(self.packageConfiguration.package_name)
        self.networkPath.setText(self.packageConfiguration.network_path)
        self.host.setText(self.packageConfiguration.host)
        self.password.setText(self.packageConfiguration.password)
        self.username.setText(self.packageConfiguration.username)
        self.ftppath.setText(self.packageConfiguration.ftp_path)
        useVCS = True if self.packageConfiguration.use_vcs=="True" else False
        self.vcs_checkbox.setChecked(useVCS)
        vcsType = configuration.VCSType.Perforce
        self.vcs_combobox.setCurrentIndex(vcsType)
        if vcsType == configuration.VCSType.Perforce:
            clientName, clientRoot = p4.getP4info()
            self.client_edit.setText(clientName)
        if self.packageConfiguration.host:
            self.connectionType.setCurrentIndex(1)
        else:
            self.connectionType.setCurrentIndex(0)

    def get_setting(self):
        self.packageConfiguration.package_name = self.packageName.text()
        self.packageConfiguration.network_path = self.networkPath.text()
        self.packageConfiguration.host = self.host.text()
        self.packageConfiguration.password = self.password.text()
        self.packageConfiguration.username = self.username.text()
        self.packageConfiguration.ftp_path = self.ftppath.text()
        self.packageConfiguration.use_vcs =self.vcs_checkbox.isChecked()
        self.packageConfiguration.vcs_type = self.vcs_combobox.currentText()
        if self.packageConfiguration.isValid():
            return self.packageConfiguration
        else:
            return None
