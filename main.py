import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo
from UI.maingui import Ui_Form  # importing our generated file


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        # super(self, MyApp).__init__()
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # call the all the btn methods
        self.btn_handler()
        # set my var
        self.path_memory_id =[]

    def btn_handler(self):
        self.ui.addfile_btn.clicked.connect(self.btn_sender)
        self.ui.preview_btn.clicked.connect(self.btn_sender)

    def btn_sender(self):
        sender_btn = self.sender().text()

        if sender_btn == "Add File(s)":
            self.path_memory_id.append(self.addfile_mth())
            self.preview_mth()
        elif sender_btn == "Add Folder":
            pass
        elif sender_btn == "Preview":
            self.preview_mth()

    def addfile_mth(self):
        try:
            # QFileDialog.getOpenFileName(self, [Title], [Directory], "[some filters]")
            # leave the dirctory blank to start the app from the running folder
            fileNames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", "C:\\Users\\H.Ali\\Desktop\\Rename test",
                                                        "All Filles (*)")

            if fileNames:
                path_memoryid = []
                for name in fileNames:
                    if len(self.path_memory_id):
                        for old_name, _, _ in self.path_memory_id:
                            if name == old_name:
                                print("you olready have this file in your list")
                            else:
                                fileName = QFileInfo(name).fileName()
                                path = QFileInfo(name).path()
                                # add item(s) to listwidget
                                item = QtWidgets.QListWidgetItem()
                                item.setText(fileName)
                                item.setCheckState(QtCore.Qt.Checked)
                                self.ui.listWidget.addItem(item)
                                # add the path and it's name  memory Id location in a list
                                memory_id = str(item).split(" ")[-1][:-1]
                                path_memoryid.append([name, path, memory_id])
        except OSError:
            pass

        if path_memoryid:
            return path_memoryid

    def preview_mth(self):
        print(self.path_memory_id)
        # add item(s) to the listview (part01)
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)

        total_row = self.ui.listWidget.count()
        a_row = self.ui.listWidget.item

        for index in range(total_row):
            if a_row(index).checkState() == QtCore.Qt.Checked:
                # add item(s) to the listview (part02) with the rename option(s)
                item = QtGui.QStandardItem(a_row(index).text())
                model.appendRow(item)
            else:
                # add item(s) to the listview (part02) don't rename
                item = QtGui.QStandardItem(a_row(index).text())
                # i need to just color the text to gray
                model.appendRow(item)

    # def moveUP(self):
    #     currentRow = self.ui.listWidget.currentRow()
    #     currentItem = self.ui.listWidget.takeItem(currentRow)
    #     self.ui.listWidget.insertItem(currentRow - 1, currentItem)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
