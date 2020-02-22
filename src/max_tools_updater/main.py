import sys
import os

# import current path
projectFolder = os.path.dirname(__file__)
if projectFolder not in sys.path:
    sys.path.append(projectFolder)

# attach debugger
from lib.sdk.debugger import *
pydev_path = "JetBrains/Toolbox/apps/PyCharm-P/ch-0/192.6262.63/helpers/pydev"
debug(pydev_path)

import loader
reload(loader)
import model.configuration
reload(model.configuration)
import controller.configurationItemView
reload(controller.configurationItemView)
loader.run()
