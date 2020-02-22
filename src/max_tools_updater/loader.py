import MaxPlus
from PySide2 import QtWidgets
import controller.mainPage as mainPage
reload(mainPage)
import pymxs
from model import configuration
import utility
import os

rt = pymxs.runtime
from lib.sdk.globals import *
import sys

import logging
from vcs.vcsManager import VCSManager

def MTU_FORCE_LOAD():
    vGlobal = rt.name("MTU_FORCE_LOAD")
    try:
        if rt.globalVars.get(vGlobal):
            return True
        else:
            return False
    except:
        return False


def run():
    try:
        home = os.path.expanduser("~")
        companyFolderName = utility.getConfig("GENERIC","CompanyFolder")
        companyFolder = os.path.join(home, companyFolderName)
        if not os.path.exists(companyFolder):
            os.makedirs(companyFolder)
        logFilePath = os.path.join(companyFolder, "maxUpdaterLog.log")

        if os.path.exists(logFilePath):
            os.remove(logFilePath)

        logging.basicConfig(level=logging.DEBUG, filename=logFilePath, filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
        # to debug in max listener
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    except:
        pass

    logging.info("Running MAX TOOL UPDATER")

    if TOOLDEBUG():
        import model.configuration
        reload(model.configuration)

        import resources.ui.config_list_ui
        reload(resources.ui.config_list_ui)
        import resources.ui.config_item_ui
        reload(resources.ui.config_item_ui)
        import resources.ui.package_view_ui
        reload(resources.ui.package_view_ui)

        import controller.configurationItemView
        reload(controller.configurationItemView)
        import controller.packageTabView
        reload(controller.packageTabView)
        import controller.settingsPage
        reload(controller.settingsPage)
        import controller.mainPage
        reload(controller.mainPage)
        reload(utility)
        import vcs.p4manager
        reload(vcs.p4manager)
        import setup.installer
        reload(setup.installer)

    mainWindow = mainPage.MainPage()
    packagesConfigurationList = configuration.PackageConfiguration.readUserPackages()
    vcsmanager = VCSManager()
    vcsmanager.packagesToUpdate = utility.getPackagesToUpdate(packagesConfigurationList)
    if MTU_FORCE_LOAD():
        mainWindow.show()
    elif len(vcsmanager.packagesToUpdate) > 0:
        mainWindow.show(bringOnTop=vcsmanager.packagesToUpdate[0])