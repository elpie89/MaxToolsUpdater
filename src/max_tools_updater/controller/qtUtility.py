from PySide2.QtWidgets import QMessageBox


def confirmRestart():
    msg = QMessageBox()

    msg.setText("Are you sure")
    msg.setInformativeText("This will restart max, are you sure?")
    msg.setWindowTitle("Max Tools Updater")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    confirmUpdate = msg.exec_()
    if confirmUpdate != QMessageBox.Ok:
        return False

    return True

def updateAllDialog():
    msg = QMessageBox()

    msg.setText("Seems like more than one package need to be updated")
    msg.setInformativeText("Do you want to update them all?")
    msg.setWindowTitle("Max Tools Updater")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    confirmUpdate = msg.exec_()
    if confirmUpdate == QMessageBox.Yes:
        return True
    return False