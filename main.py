import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo
from UI.maingui import Ui_Form  # importing our generated file


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        #super(self, MyApp).__init__()
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # call the all the btn methods
        self.btn_handler()

    def btn_handler(self):
        self.ui.addfile_btn.clicked.connect(self.btn_sender)
        self.ui.preview_btn.clicked.connect(self.btn_sender)

    def btn_sender(self):
        sender_btn = self.sender().text()

        if sender_btn == "Add File(s)":
            path_memory_id = self.addfile_mth()
        elif sender_btn == "Add Folder":
            pass

        if sender_btn == "Preview" and path_memory_id:
            self.preview_mth(path_memory_id)

    def addfile_mth(self):
        try:
            # QFileDialog.getOpenFileName(self, [Title], [Directory], "[some filters]")
            # leave the dirctory blank to start the app from the running folder
            fileNames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", "C:\\Users\\H.Ali\\Desktop\\Rename test", "All Filles (*)")

            if fileNames:
                path_memory_id = list
                for name in fileNames :
                    fileName: str = QFileInfo(name).fileName()
                    path = QFileInfo(name).path()
                    # add item(s) to listwidget
                    item = QtWidgets.QListWidgetItem()
                    item.setText(fileName)
                    item.setCheckState(QtCore.Qt.Checked)
                    self.ui.listWidget.addItem(item)
                    # add the path and it's name  memory Id location in a list
                    memory_id = str(item).split(" ")[-1][:-1]
                    path_memory_id.append([path, memory_id])
        except OSError:
            pass
        finally:
            return path_memory_id

    def preview_mth(self, path_memory_id):
        # add item(s) to the listview (part01)
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)

        for index in range(self.ui.listWidget.count()):
            if self.ui.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                # add item(s) to the listview (part02) with the rename option(s)
                item = self.ui.listWidget.item(index).text()
                model.appendRow(item)
            else:
                # add item(s) to the listview (part02) don't rename
                item = self.ui.listWidget.item(index).text()
                item.format()
                model.appendRow(item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
