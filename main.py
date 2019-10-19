import sys
import os
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
        self.ui.clear_btn.clicked.connect(self.clear_mth)
        self.ui.rename_btn.clicked.connect(self.rename_mth)

    def btn_sender(self):
        sender_btn = self.sender().text()

        if sender_btn == "Add File(s)":
            result = self.addfile_mth()
            if result:
                for name_lst in result:
                    self.path_memory_id.append(name_lst)

                self.preview_mth()
        elif sender_btn == "Add Folder":
            pass
        elif sender_btn == "Preview":
            self.preview_mth()

    def addfile_mth(self):
        # QFileDialog.getOpenFileName(self, [Title], [Directory], "[some filters]")
        # leave the dirctory blank to start the app from the running folder
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", "C:\\Users\\H.Ali\\Desktop\\Rename test",
                                                    "All Filles (*);; Video Filles (*.mkv, *.mp4, *.avi, *.ts, *.m4v)")
        path_memoryid = []
        duplicate = False
        if fileNames:
            for name in fileNames:
                if len(self.path_memory_id):
                    for old_name, _, _ in self.path_memory_id:
                        if name == old_name:
                            duplicate = True
                            print("you olready have this file in your list")
                            break

                if not duplicate:
                    fileName = QFileInfo(name).fileName()
                    path = QFileInfo(name).path()
                    # add item(s) to listwidget
                    item = QtWidgets.QListWidgetItem()
                    item.setText(fileName)
                    item.setCheckState(QtCore.Qt.Checked)
                    self.ui.listWidget.addItem(item)
                    # add the path and it's memory ID location in a list
                    memory_id = str(item).split(" ")[-1][:-1]
                    path_memoryid.append([name, path, memory_id])

        if path_memoryid:
            return path_memoryid
        else:
            return False

    def preview_mth(self):
        # add item(s) to the listview (part01)
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)

        total_row = self.ui.listWidget.count()
        a_row = self.ui.listWidget.item

        # some out of the loop option(s)
        if self.ui.serial_LE.text():
            serial = int(self.ui.serial_LE.text())

        for index in range(total_row):
            if a_row(index).checkState() == QtCore.Qt.Checked:
                name = a_row(index).text().split(".", 1)[0]
                ext = a_row(index).text().split(".")[-1]
                # add item(s) to the listview (part02) with the rename option(s)
                if self.ui.name_LE.text():
                    name = self.ui.name_LE.text()
                if self.ui.ext_LE.text():
                    ext = self.ui.ext_LE.text()
                if self.ui.serial_LE.text():
                    name = f"{name} {str(serial).zfill(len(self.ui.serial_LE.text()))}"
                    serial += 1

                # the Sub file options
                if self.ui.lang_cobox.currentText():
                    name = f"{name}.{self.ui.order_LE.text()}.{self.ui.fansub_LE.text()}.{self.ui.delay_LE.text()}.{self.ui.lang_cobox.currentText()}"
                elif self.ui.delay_LE.text():
                    name = f"{name}.{self.ui.order_LE.text()}.{self.ui.fansub_LE.text()}.{self.ui.delay_LE.text()}"
                elif self.ui.fansub_LE.text():
                    name = f"{name}.{self.ui.order_LE.text()}.{self.ui.fansub_LE.text()}"
                elif self.ui.order_LE.text():
                    name = f"{name}.{self.ui.order_LE.text()}"
                # final step to add the name to the listview
                item = QtGui.QStandardItem(f"{name}.{ext}")
                model.appendRow(item)
            else:
                # add item(s) to the listview (part02) don't rename
                item = QtGui.QStandardItem(a_row(index).text())
                # i need to just color the text to gray
                model.appendRow(item)

    def rename_mth(self):
        model = self.ui.listView.model()
        for row in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(row)
            memory_id = str(item).split(" ")[-1][:-1]
            for mem_id in self.path_memory_id:
                if memory_id in mem_id[2]:
                    path = mem_id[1].replace("/", "\\")
                    os.chdir(path)
                    os.rename(item.text(), model.item(row).text())

    def clear_mth(self):
        # clear all the item(s) in listwidget
        self.ui.listWidget.clear()
        # clear all the item(s) in listview
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)
        model.removeRows(0, model.rowCount())
        # clear the self.path_memory_id
        self.path_memory_id = []

    # def moveUP(self):
    #     currentRow = self.ui.listWidget.currentRow()
    #     currentItem = self.ui.listWidget.takeItem(currentRow)
    #     self.ui.listWidget.insertItem(currentRow - 1, currentItem)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
