import os
from pyside2uic import compileUi
import glob
import subprocess

# start project based var
projectName = "max_tools_updater"
rccCompiler = r"C:\Program Files\Autodesk\Maya2019\bin\pyside2-rcc.exe"
rawUIFolder = "ui"
rawQRCFolder = "qrc"
compiledUIFolder = "resources/ui/"
compiledRCFolder = "resources/rc/"

'''
//based on following project structure
src                         (folder)
    project_name            (folder)
        resources           (package)
            ui              (package)
            rc              (package)
    resources               (folder)
        qrc                 (folder)
        ui                  (folder)
'''
# end project based var

compilerPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.join(os.path.abspath(compilerPath), os.pardir)
dirPath = os.path.join(parentPath, projectName)

uiCompiledDest = os.path.join(dirPath, compiledUIFolder)
rcCompiledDest = os.path.join(dirPath, compiledRCFolder)

if not os.path.exists(uiCompiledDest):
    os.makedirs(uiCompiledDest)
if not os.path.exists(rcCompiledDest):
    os.makedirs(rcCompiledDest)

uiFiles = glob.glob(r"{resourcesPath}/*.ui".format(resourcesPath=os.path.join(compilerPath, rawUIFolder)))
qrcFiles = glob.glob(r"{resourcesPath}/*.qrc".format(resourcesPath=os.path.join(compilerPath, rawQRCFolder)))

for uiFilePath in uiFiles:
    fileName = os.path.basename(uiFilePath)
    name = os.path.splitext(fileName)[0]
    pyfile = open(r"{destDir}\{name}_ui.py".format(destDir=uiCompiledDest, name=name), 'w')
    compileUi(uiFilePath, pyfile, False, 4, False)
    pyfile.close()

for qrcFile in qrcFiles:
    fileName = os.path.basename(qrcFile)
    name = os.path.splitext(fileName)[0]
    pyfile = r"{outputFolder}\{outputName}_rc.py".format(outputFolder=rcCompiledDest, outputName=name)
    try:
        subprocess.call([rccCompiler, qrcFile, "-o", pyfile])
    except IOError:
        print("pyside2-rcc.exe not found")
