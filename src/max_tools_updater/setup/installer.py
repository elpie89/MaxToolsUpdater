import pymxs
import os
import subprocess
from lib.sdk.singleton import Singleton
import xml.etree.ElementTree as ET

from model.configuration import PackageConfiguration

USERPLUGINFOLDER = "userplugs"
PACKAGE_PATH_MACRO = "###PACKAGE_PATH###"


class FileInstructionInfo:
    fileType = None
    packageRelativePath = None
    fileName = None

    def __init__(self, fileType, packageRelativePath, fileName):
        self.fileType = fileType
        self.packageRelativePath = packageRelativePath
        self.fileName = fileName

    def getRelativePath(self):
        return os.path.join(self.packageRelativePath, self.fileName)


class Instruction(object):
    # todo those name are not intuitive rename it
    startupFiles = None
    cplugFiles = None
    assemblies = None
    rootlibs = None

    def __init__(self):
        self.startupFiles = list()
        self.cplugFiles = list()
        self.assemblies = list()
        self.rootlibs = list()


class Installer(object):
    __metaclass__ = Singleton

    deletePackages = None
    userPackages = None
    assemblies = None
    deletedAssemblies = None

    def __init__(self):
        self.deletePackages = list()
        self.userPackages = list()
        self.assemblies = list()
        self.deletedAssemblies = list()
        self.rootlibs = list()
        self.deletedRootlibs = list()

    def __installPackage(self, userPackage):
        '''used both for installation and for updates'''
        self.addPluginFolder()
        startupFolder = pymxs.runtime.symbolicPaths.getPathValue("$userStartupScripts")
        plugcfgFolder = self.getPluginFolder()
        xmlFile = userPackage.getInstructionFile()
        if xmlFile:
            instruction = self.parseInstruction(xmlFile)
            for startupFile in instruction.startupFiles:
                absFilePath = os.path.normpath(userPackage.getPackageFilePath(relativeFilePath=startupFile.getRelativePath()))
                destFilePath = os.path.normpath(os.path.join(startupFolder, startupFile.fileName))
                pymxs.runtime.deleteFile(destFilePath)
                f = open(absFilePath, "r")
                fileContent = f.read()
                f.close()
                scriptsFolder = os.path.normpath(os.path.join(userPackage.getPackageLocation(), "src/scripts"))
                fileContent = fileContent.replace(PACKAGE_PATH_MACRO, scriptsFolder)
                f = open(destFilePath, "w")
                f.write(fileContent)
                f.close()
            for cplugFile in instruction.cplugFiles:
                absFilePath = userPackage.getPackageFilePath(relativeFilePath=cplugFile.getRelativePath())
                destFilePath = os.path.join(plugcfgFolder, cplugFile.fileName)
                process = subprocess.Popen('del "{0}" /Q /F'.format(destFilePath), shell=True)
                process.wait()
            for assembly in instruction.assemblies:
                absFilePath = userPackage.getPackageFilePath(relativeFilePath=assembly.getRelativePath())
                absFilePath = os.path.normpath(absFilePath)
                self.assemblies.append(absFilePath)
            for rootlib in instruction.rootlibs:
                absFilePath = userPackage.getPackageFilePath(relativeFilePath=rootlib.getRelativePath())
                absFilePath = os.path.normpath(absFilePath)
                self.rootlibs.append(absFilePath)

        # write version in registry
        PackageConfiguration.savePackageVersion(userPackage.package_name, userPackage.getCurrentVersion())

    def __removePackage(self, userPackage):
        startupFolder = pymxs.runtime.symbolicPaths.getPathValue("$userStartupScripts")
        plugcfgFolder = self.getPluginFolder()
        xmlFile = userPackage.getInstructionFile()
        if xmlFile:
            instruction = self.parseInstruction(xmlFile)
            for startupFile in instruction.startupFiles:
                filePath = os.path.join(startupFolder, startupFile.fileName)
                filePath = os.path.normpath(filePath)
                os.remove(filePath)
            for cplugFile in instruction.cplugFiles:
                filePath = os.path.join(plugcfgFolder, cplugFile.fileName)
                filePath = os.path.normpath(filePath)
                os.remove(filePath)
            for assembly in instruction.assemblies:
                absFilePath = os.path.join(self.getAssembliesFolder(), assembly.fileName)
                self.deletedAssemblies.append(absFilePath)

    def reinstallPackages(self, log=False):

        self.assemblies = list()
        self.deletedAssemblies = list()
        self.rootlibs = list()
        self.deletedRootlibs = list()

        for delPackage in self.deletePackages:
            self.__removePackage(delPackage)
        for usrPackage in self.userPackages:
            self.__installPackage(usrPackage)

        addedAssembliesFiles = self.listToString(self.assemblies)
        removedAssembliesFiles = self.listToString(self.deletedAssemblies)
        addedRootlibsFiles = self.listToString(self.rootlibs)
        removedRootlibsFiles = self.listToString(self.deletedRootlibs)


        subprocess.call([self.getBatFile(), self.getAssembliesFolder(), str(log), self.getMaxExecutable(), addedAssembliesFiles, removedAssembliesFiles, addedRootlibsFiles,removedRootlibsFiles])

    def updatePackage(self, userPackage):

        self.assemblies = list()
        self.rootlibs = list()
        self.__installPackage(userPackage)
        # add assemblies and rootlib
        addedAssembliesFiles = self.listToString(self.assemblies)
        removedAssembliesFiles = self.listToString(self.deletedAssemblies)
        addedRootlibsFiles = self.listToString(self.rootlibs)
        removedRootlibsFiles = self.listToString(self.deletedRootlibs)

        subprocess.call([self.getBatFile(), self.getAssembliesFolder(), str(False), self.getMaxExecutable(), addedAssembliesFiles, removedAssembliesFiles,addedRootlibsFiles,removedRootlibsFiles])

    def listToString(self, mList):
        mString = ""
        if mList:
            for i in range(len(mList)):
                mString += mList[i]
                if i != len(mList) - 1:
                    mString += ";"
        return mString

    @staticmethod
    def getBatFile():
        batFile = os.path.join(os.path.dirname(__file__), "installer.bat")
        batFile = os.path.normpath(batFile)
        return batFile

    def addPluginFolder(self):
        maxdata = pymxs.runtime.symbolicPaths.getPathValue("$maxdata")
        pluginIni = os.path.join(maxdata, "Plugin.UserSettings.ini")
        userplugsPath = os.path.join(maxdata, USERPLUGINFOLDER)
        if not os.path.exists(userplugsPath):
            os.mkdir(userplugsPath)
        pymxs.runtime.setINISetting(pluginIni, "Directories", "Additional MAX User plug-ins", userplugsPath)

    def getPluginFolder(self):
        maxdata = pymxs.runtime.symbolicPaths.getPathValue("$maxdata")
        return os.path.join(maxdata, USERPLUGINFOLDER)

    def getAssembliesFolder(self):
        return pymxs.runtime.symbolicPaths.getPathValue("$assemblies")

    def parseInstruction(self, instructionFile):
        instruction = Instruction()
        tree = ET.parse(instructionFile)
        root = tree.getroot()
        for item in root.findall("./instruction/"):
            t = item.get("type")
            p = item.get("relativePath")
            n = item.get("name")
            fileInstructionInfo = FileInstructionInfo(fileType=t, packageRelativePath=p, fileName=n)
            if fileInstructionInfo.fileType == "startup":
                instruction.startupFiles.append(fileInstructionInfo)
            if fileInstructionInfo.fileType == "assembly":
                instruction.assemblies.append(fileInstructionInfo)
            if fileInstructionInfo.fileType == "cplug":
                instruction.cplugFiles.append(fileInstructionInfo)
            if fileInstructionInfo.fileType == "rootlib":
                instruction.rootlibs.append(fileInstructionInfo)
        return instruction

    def getMaxExecutable(self):
        dir = pymxs.runtime.GetDir(pymxs.runtime.Name("maxroot"))
        maxpath = os.path.join(dir, "3dsmax.exe")
        return os.path.normpath(maxpath)
