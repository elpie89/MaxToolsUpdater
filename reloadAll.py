import os # we use os.path.join, os.path.basename
import sys # we use sys.path
import glob # we use glob.glob
import importlib # we use importlib.import_module

projectFolder = os.path.join(os.path.dirname(__file__),"src")
sys.path.append(projectFolder) # this tells python to look in `import_folder` for imports
for src_file in glob.glob(os.path.join(projectFolder, '*.py')):
    name = os.path.basename(src_file)[:-3]
    importlib.import_module(name)
    reload(sys.modules[name])
    importlib.import_module(name)