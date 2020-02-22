import os
import tempfile
import subprocess


# to set config
# os.system('cmd /c "p4 set P4CLIENT={0}"'.format(userPackage.p4client))

def syncPackage(userPackage):
    packageFolder = userPackage.getPackageLocation()
    os.system('cmd /c "p4 sync {0}...#head"'.format(packageFolder))


def readDepotFile(filePath):
    if os.path.exists(filePath):
        os.system('cmd /c "p4 print -q {0}#head" > {1}/tmp.xml'.format(filePath, tempfile.gettempdir()))
        return unicode(os.path.normpath("{0}/tmp.xml".format(tempfile.gettempdir())))


def getP4info():
    """
    :return:
    clientName, clientRootFolder
    """
    cmd = "p4 info"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = process.communicate()
    exit_code = process.returncode
    if exit_code == 0:
        info = dict()
        datas = stdoutdata.split("\r\n")
        for data in datas:
            if data:
                key = data.split(": ")[0]
                value = data.split(": ")[1]
                info.update({key: value})
        return info["Client name"], info["Client root"]

