import ast
import os
import pathlib
import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QAbstractItemView

from UI.maingui import Ui_Form  # importing our generated file


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        # super(self, MyApp).__init__()
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # set Some Var
        self.original_name_lst = []
        self.new_name_lst = []
        self.tmp_path = "C:\\Users\\H.Ali\\Desktop\\Rename Test\\"

        # set serial_LE, Order_LE, and delay_LE to eccept only Integer numbers
        onlyInt = QIntValidator()
        self.ui.serial_LE.setValidator(onlyInt)
        self.ui.order_LE.setValidator(onlyInt)
        self.ui.delay_LE.setValidator(onlyInt)

        # call the all the method(s)
        self.hide_unhide_col()
        self.btn_handler()
        self.preset_cobox_mth()

        # setup table widget and Column(s)
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
        self.ui.addfolder_btn.clicked.connect(self.addfile_mth)
        self.ui.addpreset_btn.clicked.connect(self.addpreset_mth)
        self.ui.clear_btn.clicked.connect(self.clear_mth)
        self.ui.rename_btn.clicked.connect(self.rename_mth)
        self.ui.unrename_btn.clicked.connect(self.unrename_mth)
        # call preview_mth for any user input
        self.ui.name_LE.textChanged.connect(self.preview_mth)
        self.ui.serial_LE.textChanged.connect(self.preview_mth)
        self.ui.ext_LE.textChanged.connect(self.preview_mth)
        self.ui.order_LE.textChanged.connect(self.preview_mth)
        self.ui.fansub_LE.textChanged.connect(self.preview_mth)
        self.ui.delay_LE.textChanged.connect(self.preview_mth)
        self.ui.lang_cobox.currentIndexChanged.connect(self.preview_mth)
        # hide or unhide the Date and Type column
        self.ui.date_chbox.clicked.connect(self.hide_unhide_col)
        self.ui.type_chbox.clicked.connect(self.hide_unhide_col)
        # call the preview_mth if the raw(s) order change
        self.ui.tableWidget.itemChanged.connect(self.reset_sort)
        # add a custom ContextMenu to the qTableWidget
        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.on_customContextMenuRequested)
        # call the sort column if the user click the column header
        self.ui.tableWidget.horizontalHeader().sortIndicatorChanged.connect(self.sort_col)

    def userinput_mth(self):
        nameLE = self.ui.name_LE.text()
        serialLE = self.ui.serial_LE.text()
        extLE = self.ui.ext_LE.text()
        orderLE = self.ui.order_LE.text()
        fansubLE = self.ui.fansub_LE.text()
        delayLE = self.ui.delay_LE.text()
        langCobox = self.ui.lang_cobox.currentText()

        return [nameLE, serialLE, extLE, orderLE, fansubLE, delayLE, langCobox]

    def addfile_mth(self):
        # read the btn name
        btn_name = self.sender().text()

        # check the name of the btn that the user clicked, then save the file(s) name in a list
        if btn_name == "Add File(s)":
            # TODO: move the option in new var
            #  I will make a var in the __ini__ def that contain the option file exe
            fileNames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", "C:\\Users\\H.Ali\\Desktop\\Rename test",
                                                        "All Filles (*);; Video Filles (*.mkv, *.mp4, *.avi, *.ts, *.m4v)")
        else:
            folder_name = QFileDialog.getExistingDirectory(self, "Add File(s) from Folder")
            # see if the user select a folfe or not
            if folder_name:
                os.chdir(folder_name)
                my_current_dic = os.getcwd()
                # the filter is easy but give me a an object
                # so I will use list comprehension version for fast check to see if the folder is empty or not
                # fileNames = filter(os.path.isfile, os.listdir(my_current_dic))
                fileNames = [f for f in os.listdir(my_current_dic) if os.path.isfile(f)]
                # TODO: make a foldernames var
                #  I will add the folder(s) name in the tbl and uncheak them by defualt
                #  and add two contextmenu to select all the rows or unselect all
                #  and maybe select folder name only or select file name only
                #  and see if I can make select files by there exe

                # see if the folder is empty or not
                if not fileNames:
                    print("The Folder is Empty or has only Folder(s)!!")
            else:
                # if the user cacel the select dialog I have to asign False
                # or the fileNames will be undefined and the program will crash
                fileNames = False

        # start the adding name(s) to the table
        duplicate = False
        if fileNames:
            # enable the clear_btn
            self.ui.clear_btn.setEnabled(True)

            # start tacking name by name from the fileNames list
            for name in fileNames:

                # check if the file has added before or not
                if self.ui.tableWidget.rowCount():
                    for row in range(self.ui.tableWidget.rowCount()):
                        if name == self.ui.tableWidget.item(row, 3).text():
                            duplicate = True
                            print("you olready have this file in your list")
                            break

                # adding the name to the table if it not there before
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

                    # resize the columns & rows to fit the text
                    self.ui.tableWidget.resizeColumnsToContents()
                    self.ui.tableWidget.resizeRowsToContents()

    def preview_mth(self):
        # the information  I need is the Total row(s) and the name of the file
        total_row = self.ui.tableWidget.rowCount()
        a_row = self.ui.tableWidget.item

        ################################################
        # the main adding to the listview is from here #
        ################################################
        # add item(s) to the listview (part01)
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)

        # some out of the loop option(s)
        if self.ui.serial_LE.text():
            serial = int(self.ui.serial_LE.text())

        unchecked = 0
        test_names = []
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

                # check if this name is duplicated or not
                if item.text() not in test_names:
                    test_names.append(item.text())
                else:
                    item.setBackground(Qt.red)
                    item.setForeground(Qt.white)

                model.appendRow(item)
            else:
                # add item(s) to the listview (part02) don't rename
                item = QtGui.QStandardItem(a_row(index, 0).text())
                item.setForeground(Qt.red)
                model.appendRow(item)
                unchecked += 1

        # this code is just to enable the addpreset_btn & rename_btn
        # first join the string from the return list then get the length
        userfield_len = len("".join(self.userinput_mth()))
        if userfield_len == 0 or unchecked == total_row:
            self.ui.rename_btn.setEnabled(False)
            self.ui.addpreset_btn.setEnabled(False)
        elif total_row > 0:
            self.ui.rename_btn.setEnabled(True)
            self.ui.addpreset_btn.setEnabled(True)

        # to make sur the row(s) and column(s) size same as the contents
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def rename_mth(self):
        model = self.ui.listView.model()
        total_rows = self.ui.tableWidget.rowCount()
        a_row = self.ui.tableWidget.item

        # check if the new names are not duplicated before the rename
        test_names = []
        duplicated = False
        for index in range(total_rows):
            if a_row(index, 0).checkState() == QtCore.Qt.Checked:
                listview_name = model.item(index).text()
                # TODO: test a different way to check if there is a duplicated name(s)
                # print(model.item(index).backgroun())
                if listview_name not in test_names:
                    test_names.append(listview_name)
                else:
                    print("you have duplicted names!! please check yuor input.")
                    duplicated = True
                    break

        if not duplicated:
            for index in range(total_rows):
                if a_row(index, 0).checkState() == QtCore.Qt.Checked:
                    # 0 is the 'Name' column
                    original_name = self.ui.tableWidget.item(index, 0).text()
                    new_name = model.item(index).text()
                    # num 3 is the full name column that have the full pathname
                    full_name = self.ui.tableWidget.item(index, 3).text()
                    path = QFileInfo(full_name).path().replace("/", "\\")
                    # chang to the path dir and then rename
                    os.chdir(path)
                    os.rename(original_name, new_name)

                    # add the original_name and the new_name to two list so i can use them in unrename_mth
                    self.original_name_lst.append(original_name)
                    self.new_name_lst.append(new_name)

                    # to disable the rename_btn and then enable the unrename_btn
                    self.ui.rename_btn.setEnabled(False)
                    self.ui.unrename_btn.setEnabled(True)
                    # TODO: see if you want this else or not????
                else:
                    print("I have to disable the Rename btn !!!!!????")

    def unrename_mth(self):
        for i in range(len(self.original_name_lst)):
            os.rename(self.new_name_lst[i], self.original_name_lst[i])

        # clear the lists value(s)
        self.new_name_lst.clear()
        self.original_name_lst.clear()

        # to disable the unrename_btn and enable the rename_btn
        self.ui.rename_btn.setEnabled(True)
        self.ui.unrename_btn.setEnabled(False)

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

    def sort_col(self):
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.setSortingEnabled(False)
        self.ui.tableWidget.horizontalHeader().setSortIndicatorShown(True)

        self.preview_mth()

    def reset_sort(self):
        # to remove the sor Indecator arrow if i manually order the rows
        self.ui.tableWidget.horizontalHeader().setSortIndicatorShown(False)

        self.preview_mth()

    def addpreset_mth(self):
        # add the 7 var in a txt file or something like it
        # maybe I will use dic??

        # call the userinput_mth to collecate the user input information
        userinput_info_lst = self.userinput_mth()

        # write the userinput information in the userinput_preset file
        with open(f"{self.tmp_path}userinput_presets.pset", "r+") as preset:
            # set the preset limit to 10 preset only
            if len(preset.readlines()) < 10:
                # TODO: Qdailog ask the user for the preset name,
                #  by defualt I will take the name_le.text() as the name
                preset_dic = {"Preset Name": userinput_info_lst[0], "Preset info": userinput_info_lst}
                preset.write(str(preset_dic) + "\n")
            else:
                # TODO: Qdailog
                print(
                    "you reach the max limit of preset option!!! pleae delete one or more preset from the preset droplist")

    def preset_cobox_mth(self):
        try:
            with open(f"{self.tmp_path}userinput_presets.pset", "r") as preset:
                for line in preset.readlines():
                    print("test")
                    # the literal_eval() mth from ast is to convert back the text line from str to dict
                    line = ast.literal_eval(line)
                    self.ui.preset_cobox.addItem(line["Preset Name"])
        except FileNotFoundError:
            # only creat the file if it not exists
            with open(f"{self.tmp_path}userinput_presets.pset", "x"):
                pass

    def on_customContextMenuRequested(self, pos):
        # if there is no table return and don't show the contextMenu
        it = self.ui.tableWidget.itemAt(pos)
        if it is None: return

        # creat the contextMenu and add the action the popup the menu in the position of the mouse
        menu = QtWidgets.QMenu()
        delete_selected_action = menu.addAction("Delete Selected Name(s)")
        delete_unselected_action = menu.addAction("Delete unSelected Name(s)")
        action = menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))

        # delete the row(s)
        total_rows = self.ui.tableWidget.rowCount()
        row = self.ui.tableWidget
        cell = self.ui.tableWidget.item

        if action == delete_selected_action:
            for index in reversed(range(total_rows)):
                if cell(index, 0).checkState() == QtCore.Qt.Checked:
                    row.removeRow(index)

        if action == delete_unselected_action:
            for index in reversed(range(total_rows)):
                if cell(index, 0).checkState() != QtCore.Qt.Checked:
                    row.removeRow(index)

        # update the listview after the delete
        self.preview_mth()

        # disable the clear_btn if there is no rows
        if self.ui.tableWidget.rowCount() == 0:
            self.ui.clear_btn.setEnabled(False)

    # TODO: maybe creat a def to move rows by keyboard??
    # def moveUP(self):
    #     currentRow = self.ui.listWidget.currentRow()
    #     currentItem = self.ui.listWidget.takeItem(currentRow)
    #     self.ui.listWidget.insertItem(currentRow - 1, currentItem)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
