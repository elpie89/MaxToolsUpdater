import logging
import os
import xml.etree.ElementTree as et
import utility
import tempfile
import ftplib
from PySide2.QtWidgets import QMessageBox
import MaxPlus
from ConfigParser import ConfigParser, RawConfigParser
from pymxs import runtime as rt

CONFIGSECTIONAME = "PACKAGE_CONFIGURATION"


class ConnectionType():
    LOCAL = 0
    FTP = 1


class VCSType():
    Perforce = 0

    @staticmethod
    def stringToVCS_Type(value):
        if value == "Perforce":
            return VCSType.Perforce
        return None


class PackageConfiguration:

    def __init__(self):
        self.package_name = None
        self.packageVersion = None
        self.connection_type = ConnectionType.LOCAL
        self.network_path = None
        self.host = None
        self.username = None
        self.password = None
        self.ftp_path = None
        self.use_vcs = False
        self.vcs_type = VCSType.Perforce

    def set_ftp_connection(self):
        self.connection_type = ConnectionType.FTP
        logging.info(self.connection_type)

    def set_local_network_connection(self):
        self.connection_type = ConnectionType.LOCAL
        logging.info(self.connection_type)

    def isValid(self):
        if self.package_name:
            if self.connection_type == ConnectionType.LOCAL:
                if self.network_path is not None:
                    return True
            else:
                if self.host and self.username and self.password and self.ftp_path:
                    return True
        return False

    def getPackageLocation(self):
        packagePath = os.path.join(self.network_path, self.package_name)
        if os.path.isabs(self.network_path):
            return packagePath
        else:
            return os.path.join(rt.pathConfig.getCurrentProjectFolder(), packagePath)

    def getMarkDown(self):
        packageLocation = self.getPackageLocation()
        changelog = os.path.join(packageLocation, "changelog.md")
        return changelog

    def getInstructionFile(self):
        packageLocation = self.getPackageLocation()
        xmlFile = os.path.join(packageLocation, "version.xml")
        return xmlFile

    def getCurrentVersion(self):
        xmlFile = self.getInstructionFile()
        if os.path.exists(xmlFile):
            try:
                xmlContent = et.parse(xmlFile)
                root = xmlContent.getroot()
                for element in root:
                    if element.tag == "updater_version":
                        return element.text
            except:
                logging.info("impossible to get version info from " + xmlFile)
        else:
            logging.info("missing file" + xmlFile)

    def getUserVersion(self):
        return self.packageVersion

    def getPackageImage(self):
        packageLocation = self.getPackageLocation()
        return os.path.join(packageLocation, "packageImage.jpg")

    def getPackageFilePath(self, relativeFilePath):
        return os.path.join(self.getPackageLocation(), relativeFilePath)

    @staticmethod
    def getCurrentVersion2(packageConfig):
        try:
            if packageConfig.connection_type == ConnectionType.LOCAL:
                server_folder = packageConfig.network_path
                server_folder = os.path.join(server_folder, packageConfig.package_name)
                serverFileVersion = os.path.join(server_folder, "version.xml")
                version = utility.get_release_version(serverFileVersion)
                return version

            if packageConfig.connection_type == ConnectionType.FTP:
                fileName = "version.xml"
                tempDownload = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
                filePath = os.path.abspath(tempDownload.name)
                gFile = open(filePath, "wb")
                ftps = ftplib.FTP_TLS(packageConfig.host)
                ftps.login(packageConfig.username,
                           packageConfig.password)  # login anonymously before securing control channel
                ftps.prot_p()  # switch to secure data connection.. IMPORTANT! Otherwise, only the user and password is encrypted and not all the file data.
                ftps.cwd("{0}/{1}/".format(packageConfig.ftp_path, packageConfig.package_name))

                ftps.retrbinary('RETR ' + fileName, gFile.write, 1024)
                ftps.quit()
                gFile.flush()
                gFile.close()
                return utility.get_release_version(filePath)
        except:
            msg = QMessageBox(MaxPlus.GetQMaxMainWindow())
            msg.setText(
                "Impossible to retrieve a connection for package {0}.\nMake sure connection settings are valids".format(
                    packageConfig.package_name))
            msg.show()

    @staticmethod
    def downloadServerFolder(packageConfig):
        if packageConfig.connection_type == ConnectionType.LOCAL:
            server_folder = packageConfig.network_path
            server_folder = os.path.join(server_folder, packageConfig.package_name)
            return os.path.normpath(utility.copyNetworkFolderToTemp(server_folder, packageConfig.package_name))

        if packageConfig.connection_type == ConnectionType.FTP:
            host = packageConfig.host
            username = packageConfig.username
            password = packageConfig.password
            ftp_path = packageConfig.ftp_path
            folder = packageConfig.package_name
            return os.path.normpath(utility.copyFTPFolderToTemp(host, username, password, ftp_path, folder))
        return None

    @staticmethod
    def getSettingsFile():
        projectFolder = rt.pathConfig.getCurrentProjectFolder()
        maxtoolupdaterSettingsFile = os.path.join(projectFolder, "packagesConfig.mtu")
        return maxtoolupdaterSettingsFile

    @staticmethod
    def saveUserPackages(packagesConfiguration):

        settings = RawConfigParser()
        for i in range(len(packagesConfiguration)):
            settings.add_section(CONFIGSECTIONAME)
            settings.set(CONFIGSECTIONAME, "PackageName", packagesConfiguration[i].package_name)
            settings.set(CONFIGSECTIONAME, "Location", packagesConfiguration[i].network_path)
            settings.set(CONFIGSECTIONAME, "PackageVersion", packagesConfiguration[i].getCurrentVersion())
            settings.set(CONFIGSECTIONAME, "Connection Type", "Local")
            settings.set(CONFIGSECTIONAME, "UseVCS", packagesConfiguration[i].use_vcs)
            settings.set(CONFIGSECTIONAME, "VCSType", packagesConfiguration[i].vcs_type)

            if packagesConfiguration[i].connection_type == ConnectionType.FTP:
                settings.set(CONFIGSECTIONAME, "Host", packagesConfiguration[i].host)
                settings.set(CONFIGSECTIONAME, "Username", packagesConfiguration[i].username)
                settings.set(CONFIGSECTIONAME, "Password", packagesConfiguration[i].password)
                settings.set(CONFIGSECTIONAME, "FTP Path", packagesConfiguration[i].ftp_path)

        with open(PackageConfiguration.getSettingsFile(), 'wb') as configfile:
            settings.write(configfile)

    @staticmethod
    def savePackageVersion(packageName, version):
        settings = RawConfigParser()
        settings.read(PackageConfiguration.getSettingsFile())
        for section in settings.sections():
            if settings.get(section, "PackageName") == packageName:
                settings.set(section, "PackageVersion", version)
        with open(PackageConfiguration.getSettingsFile(), 'wb') as configfile:
            settings.write(configfile)

    @staticmethod
    def readUserPackages():
        settings = RawConfigParser()
        settings.read(PackageConfiguration.getSettingsFile())
        packagesConfiguration = []
        for section in settings.sections():
            config = PackageConfiguration()
            config.package_name = settings.get(section, "PackageName")
            config.packageVersion = settings.get(section, "PackageVersion")
            config.network_path = settings.get(section, "Location")
            config.connection_type = ConnectionType.LOCAL  # ConnectionType(settings.value("Connection Type"))
            config.host = settings.get(section, "Host")
            config.username = settings.get(section, "Username")
            config.password = settings.get(section, "Password")
            config.ftp_path = settings.get(section, "FTP Path")
            config.use_vcs = True if settings.get(section, "UseVCS") == "True" else False
            config.vcs_type = VCSType.stringToVCS_Type(settings.get(section, "VCSType"))
            packagesConfiguration.append(config)
        return packagesConfiguration
