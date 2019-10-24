import os
import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

from UI.maingui import Ui_Form  # importing our generated file


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        # super(self, MyApp).__init__()
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # call the all the method(s)
        self.hide_unhide_col()
        self.btn_handler()
        # setup table widget and Column(s)
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Name", "Date", "Type", "Full Name"])
        self.ui.tableWidget.setColumnHidden(1, True)
        self.ui.tableWidget.setColumnHidden(2, True)
        self.ui.tableWidget.setColumnHidden(3, True)
        # set btn stats
        self.ui.addpreset_btn.setEnabled(False)
        self.ui.rename_btn.setEnabled(False)
        self.ui.unrename_btn.setEnabled(False)
        self.ui.clear_btn.setEnabled(False)

    def btn_handler(self):
        self.ui.addfile_btn.clicked.connect(self.addfile_mth)
        self.ui.clear_btn.clicked.connect(self.clear_mth)
        self.ui.rename_btn.clicked.connect(self.rename_mth)
        self.ui.name_LE.textChanged.connect(self.preview_mth)
        self.ui.serial_LE.textChanged.connect(self.preview_mth)
        self.ui.ext_LE.textChanged.connect(self.preview_mth)
        self.ui.order_LE.textChanged.connect(self.preview_mth)
        self.ui.fansub_LE.textChanged.connect(self.preview_mth)
        self.ui.delay_LE.textChanged.connect(self.preview_mth)
        self.ui.lang_cobox.currentIndexChanged.connect(self.preview_mth)
        self.ui.date_chbox.clicked.connect(self.hide_unhide_col)
        self.ui.type_chbox.clicked.connect(self.hide_unhide_col)
        self.ui.tableWidget.itemChanged.connect(self.preview_mth)

    def addfile_mth(self):
        # QFileDialog.getOpenFileName(self, [Title], [Directory], "[some filters]")
        # leave the dirctory blank to start the app from the running folder
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", "C:\\Users\\H.Ali\\Desktop\\Rename test",
                                                    "All Filles (*);; Video Filles (*.mkv, *.mp4, *.avi, *.ts, *.m4v)")

        duplicate = False
        if fileNames:
            # enable the clear_btn
            self.ui.clear_btn.setEnabled(True)

            for name in fileNames:
                # check if the file has added before or not
                if self.ui.tableWidget.rowCount():
                    for row in range(self.ui.tableWidget.rowCount()):
                        if name == self.ui.tableWidget.item(row, 3).text():
                            duplicate = True
                            print("you olready have this file in your list")
                            break

                if not duplicate:
                    modificationTime = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(name)))
                    fileName = QFileInfo(name).fileName()
                    ext_type = QFileInfo(name).suffix()
                    # setup table widget Row(s)
                    row_position = self.ui.tableWidget.rowCount()
                    self.ui.tableWidget.insertRow(row_position)
                    self.ui.tableWidget.verticalHeader().setVisible(False)
                    # add item(s) to the table
                    self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(fileName))
                    self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(modificationTime))
                    self.ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(ext_type))
                    self.ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(name))
                    # set some option(s) to the item
                    for a_row in range(row_position + 1):
                        for a_col in range(self.ui.tableWidget.columnCount()):
                            if a_col == 0:
                                self.ui.tableWidget.item(a_row, a_col).setCheckState(Qt.Checked)

                            self.ui.tableWidget.item(a_row, a_col).setFlags(
                                Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

                    self.ui.tableWidget.resizeColumnsToContents()
                    self.ui.tableWidget.resizeRowsToContents()

    def preview_mth(self):
        # the information  I need is the Total row(s) and the name of the file
        total_row = self.ui.tableWidget.rowCount()
        a_row = self.ui.tableWidget.item

        # to enable the rename btn
        if len(self.ui.name_LE.text()) + len(self.ui.serial_LE.text()) + len(self.ui.ext_LE.text()) + len(
                self.ui.order_LE.text()) + len(self.ui.fansub_LE.text()) + len(self.ui.delay_LE.text()) + len(
                self.ui.lang_cobox.currentText()) >= 1:
            self.ui.rename_btn.setEnabled(True)
        else:
            self.ui.rename_btn.setEnabled(False)

        ################################################
        # the main adding to the listview is from here #
        ################################################
        # add item(s) to the listview (part01)
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)

        # some out of the loop option(s)
        if self.ui.serial_LE.text():
            serial = int(self.ui.serial_LE.text())

        unchecked_name = 0
        for index in range(total_row):
            if a_row(index, 0).checkState() == QtCore.Qt.Checked:
                # I can use the QFileInfo but I will leave it as alternative way
                name = ".".join(a_row(index, 0).text().rsplit(".")[:-1])
                ext = a_row(index, 0).text().split(".")[-1]
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
                item = QtGui.QStandardItem(a_row(index, 0).text())
                item.setForeground(Qt.red)
                model.appendRow(item)
                unchecked_name += 1
                print(unchecked_name)
                if unchecked_name == total_row:
                    self.ui.rename_btn.setEnabled(False)
                    self.ui.unrename_btn.setEnabled(False)

    def rename_mth(self):
        model = self.ui.listView.model()
        total_rows = self.ui.tableWidget.rowCount()
        a_row = self.ui.tableWidget.item

        for index in range(total_rows):
            if a_row(index, 0).checkState() == QtCore.Qt.Checked:
                # 0 is the Name column
                original_name = self.ui.tableWidget.item(index, 0).text()
                new_name = model.item(index).text()
                # num 3 is the full name column that have the full pathname
                full_name = self.ui.tableWidget.item(index, 3).text()
                path = QFileInfo(full_name).path().replace("/", "\\")
                # chang to the path dir and then rename
                os.chdir(path)
                os.rename(original_name, new_name)

                # to disable the rename_btn and then enable the unrename_btn
                self.ui.rename_btn.setEnabled(False)
                self.ui.unrename_btn.setEnabled(True)
            else:
                print("I have to disable the Rename btn !!!!!????")

    def clear_mth(self):
        # clear all the item(s) in tablewidget
        rows = self.ui.tableWidget.rowCount()
        for index in reversed(range(rows)):
            self.ui.tableWidget.removeRow(index)

        # clear all the item(s) in listview
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)
        model.removeRows(0, model.rowCount())

        # clear all the user input(s)
        self.ui.name_LE.clear()
        self.ui.serial_LE.clear()
        self.ui.ext_LE.clear()
        self.ui.order_LE.clear()
        self.ui.fansub_LE.clear()
        self.ui.delay_LE.clear()
        self.ui.lang_cobox.setCurrentIndex(0)

        # disable the clear_btn
        self.ui.clear_btn.setEnabled(False)

    def hide_unhide_col(self):

        if self.ui.date_chbox.isChecked():
            self.ui.tableWidget.setColumnHidden(1, False)
            self.ui.tableWidget.resizeColumnsToContents()
        else:
            self.ui.tableWidget.hideColumn(1)

        if self.ui.type_chbox.isChecked():
            self.ui.tableWidget.setColumnHidden(2, False)
            self.ui.tableWidget.resizeColumnsToContents()
        else:
            self.ui.tableWidget.hideColumn(2)

    # def moveUP(self):
    #     currentRow = self.ui.listWidget.currentRow()
    #     currentItem = self.ui.listWidget.takeItem(currentRow)
    #     self.ui.listWidget.insertItem(currentRow - 1, currentItem)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
