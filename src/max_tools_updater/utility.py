import errno
import xml.etree.ElementTree as et
import os
import tempfile
import distutils.dir_util
import distutils.file_util
import shutil
import ftplib
import lib.external.ftp_utility as ftp_utility
import time
import sys
import pymxs
import vcs.p4manager as p4manager
import ConfigParser

rt = pymxs.runtime

import logging


def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    configFile = os.path.join(os.path.dirname(__file__), "config.cfg")
    config.read(configFile)
    return config.get(section, key)


def get_release_version(versionFile):
    if os.path.exists(versionFile):
        try:
            version_file = et.parse(versionFile)
            root = version_file.getroot()
            for element in root:
                if element.tag == "updater_version":
                    return element.text
        except:
            logging.info("impossible to get version info from " + versionFile)
    else:
        logging.info("missing file" + versionFile)


def isPackageUpdated(local_version, public_version):
    loc_v = int(local_version.replace(".", ""))
    if public_version:
        pub_v = int(public_version.replace(".", ""))
        if loc_v < pub_v:
            return False
    return True


def arePackagesUpdated(packagesConfigurationList):
    if not packagesConfigurationList:
        return True
    else:
        for i in range(len(packagesConfigurationList)):
            packageConfig = packagesConfigurationList[i]
            userVersion = packageConfig.getUserVersion()
            currentVersion = getServerVersion(packageConfig)
            if not isPackageUpdated(userVersion, currentVersion):
                return False
    return True


def getPackagesToUpdate(packagesConfigurationList):
    result = []
    if not packagesConfigurationList:
        return result
    else:
        for i in range(len(packagesConfigurationList)):
            packageConfig = packagesConfigurationList[i]
            userVersion = packageConfig.getUserVersion()
            currentVersion = getServerVersion(packageConfig)
            if not isPackageUpdated(userVersion, currentVersion):
                result.append(packageConfig)
    return result


def logMaxSymbolicValues():
    for i in range(1, pymxs.runtime.symbolicPaths.numPaths()):
        sim = pymxs.runtime.symbolicPaths.getPathName(i)
        print sim
        print pymxs.runtime.symbolicPaths.getPathValue(sim)


def getBatScript(scriptName):
    path = os.path.join(os.path.dirname(__file__), scriptName)
    return os.path.abspath(path)


def parseUpdateInstruction(tempPackagePath):
    installationInfo = os.path.join(tempPackagePath, "version.xml")
    if os.path.exists(installationInfo):
        outsidePackageInfo = []
        try:
            version_file = et.parse(installationInfo)
            root = version_file.getroot()
            instruction = root[1]
            for element in instruction:
                if element.tag == "file":
                    outsidePackageInfo.append(element.attrib)

            return outsidePackageInfo
        except:
            logging.info("impossible to parse" + installationInfo)
            return

    else:
        logging.info("missing Installation INFO file" + installationInfo)


def copyFile(srcFolder, dstFolder, fileName):
    srcFile = os.path.join(srcFolder, fileName)
    dstFile = os.path.join(dstFolder, fileName)
    if os.path.exists(srcFolder) and os.path.exists(srcFile) and os.path.exists(dstFolder):
        if os.path.exists(dstFile):
            try:
                os.remove(dstFile)
            except:
                logging.info("Permission Denied")
        shutil.copy(srcFile, dstFile)


def copyNetworkFolderToTemp(networkFolderPath, packageName):
    dirpath = tempfile.mkdtemp()
    tempPackageDir = os.path.join(dirpath, packageName)
    logging.info("copying from network " + networkFolderPath + " to " + tempPackageDir)
    copied = distutils.dir_util.copy_tree(networkFolderPath, tempPackageDir)
    for f in copied:
        logging.info("copied: " + f)
    logDirectoryContent(dirpath)
    return tempPackageDir


def copyFTPFolderToTemp(host, user, password, ftpPath, packageName):
    dirPath = tempfile.mkdtemp()
    tempPackageDir = os.path.join(dirPath, packageName)

    ftps = ftplib.FTP_TLS(host)
    ftps.login(user, password)  # login anonymously before securing control channel
    ftps.prot_p()  # switch to secure data connection.. IMPORTANT! Otherwise, only the user and password is encrypted and not all the file data.
    ftps.cwd(r"{0}/".format(ftpPath))
    ftp_utility.download_ftp_tree(ftps, packageName, dirPath, overwrite=True)
    return tempPackageDir


def downloadFiles(ftp, interval, path, destination):
    try:
        ftp.cwd(path)
        os.chdir(destination)

        mkdir_p(os.path.join(destination, path))
        logging.info("Created: " + os.path.join(destination, path))
    except OSError:
        pass
    except ftplib.error_perm:
        logging.info("Error: could not change to " + path)
        sys.exit("Ending Application")

    filelist = ftp.nlst()

    for file in filelist:
        time.sleep(interval)
        try:
            srcPath = path + file + "/"
            ftp.cwd(srcPath)
            downloadFiles(ftp, interval, srcPath, destination)
        except ftplib.error_perm:
            fileDir = os.path.join(destination, path)
            os.chdir(fileDir)
            filePath = os.path.join(fileDir, file)
            try:
                ftp.retrbinary("RETR " + file, open(filePath, "wb").write)
                logging.info("Downloaded: " + file)
            except:
                logging.info("Error: File could not be downloaded " + file)
    return


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def logDirectoryContent(directoryPath):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(directoryPath):
        for file in f:
            files.append(os.path.join(r, file))

    for f in files:
        logging.info((f))


def getMaxPath():
    dir = rt.GetDir(pymxs.runtime.Name("maxroot"))
    return os.path.normpath(dir)


def getLocalInstructionFile(packagePath):
    instructionFile = os.path.join(packagePath, "version.xml")
    return instructionFile


def getServerVersion(packageConfig):
    instructionFile = packageConfig.getInstructionFile()
    serverFileInstruction = p4manager.readDepotFile(instructionFile)
    try:
        version_file = et.parse(serverFileInstruction)
        root = version_file.getroot()
        for element in root:
            if element.tag == "updater_version":
                return element.text
    except:
        logging.info("impossible to get version info from " + instructionFile + "at head")
    os.remove(serverFileInstruction)
