import ast
import datetime
import os
import sys
import time
import traceback

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QInputDialog, QLineEdit, QMessageBox, QStyle

from UI.maingui import Ui_Form  # importing our generated file


def msgbox_dailog_mth(msginfo_lst):
    msg = QMessageBox()
    msg.setIcon(msginfo_lst[0])

    msg.setWindowTitle(msginfo_lst[1])
    msg.setText(msginfo_lst[2])
    msg.setInformativeText(msginfo_lst[3])
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        # super(self, MyApp).__init__()
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # set btn icon
        self.ui.erase_btn.setIcon(QIcon("icons/eraser_on.png"))
        self.ui.x_btn.setIcon(QIcon("icons/delete_on.ico"))
        # Icon Farm-fresh made by FatCow Web Hosting from www.iconfinder.com
        # https://www.iconfinder.com/icons/36060/add_folder_icon
        self.ui.addfolder_btn.setIcon(QIcon("icons/add_folder.png"))
        # https://www.iconfinder.com/icons/36242/add_page_icon
        self.ui.addfile_btn.setIcon(QIcon("icons/add_file.png"))

        # set Some Var
        self.original_name_lst = []
        self.new_name_lst = []
        self.tmp_path = ""

        # set serial_LE, Order_LE, and delay_LE to eccept only Integer numbers
        onlyInt = QIntValidator()
        self.ui.serial_LE.setValidator(onlyInt)
        self.ui.order_LE.setValidator(onlyInt)
        self.ui.delay_LE.setValidator(onlyInt)

        # call the all the method(s)
        self.hide_unhide_col()
        self.btn_handler()
        self.preset_history_cobox_mth("userinput.pset")
        self.preset_history_cobox_mth("history.pset")

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
        self.ui.erase_btn.setEnabled(False)
        self.ui.x_btn.setEnabled(False)

    def btn_handler(self):
        self.ui.addfile_btn.clicked.connect(self.addfile_mth)
        self.ui.addfolder_btn.clicked.connect(self.addfile_mth)
        self.ui.addpreset_btn.clicked.connect(lambda file_name: self.addpreset_history_mth("userinput.pset"))
        self.ui.clear_btn.clicked.connect(self.clear_mth)
        self.ui.rename_btn.clicked.connect(self.rename_mth)
        self.ui.unrename_btn.clicked.connect(self.unrename_mth)
        self.ui.preset_cobox.currentIndexChanged.connect(self.set_preset_mth)
        self.ui.log_cobox.currentIndexChanged.connect(self.set_preset_mth)
        # call icon btn mth
        self.ui.erase_btn.clicked.connect(lambda set_lst: self.set_fields_mth("erase"))
        self.ui.x_btn.clicked.connect(self.del_preset_mth)
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
            fileNames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", self.tmp_path,
                                                        "All Filles (*);; Video Filles (*.mkv, *.mp4, *.avi, *.ts, *.m4v)")
        else:
            folder_name = QFileDialog.getExistingDirectory(self, "Select Folder", self.tmp_path)
            # see if the user select a folfe or not
            if folder_name:
                os.chdir(folder_name)
                my_current_dir = os.getcwd()

                # see if the folder is empty or not
                if len(os.listdir(folder_name)) == 0:
                    msginfo_lst = [QMessageBox.Warning, "Empty Folder Warning",
                                   "The Folder is Empty!!",
                                   "No File Or Folder will be added."]
                    msgbox_dailog_mth(msginfo_lst)

                    # if the user cancel the select dialog I have to asign False
                    # or the fileNames will be undefined and the program will crash
                    fileNames = False
                else:
                    # make the name(s) in fileNames list look the same as the format from the getOpenFileNames
                    cwdpath = my_current_dir.replace("\\", "/")
                    fileNames = []
                    for f_name in os.listdir(my_current_dir):
                        fileNames.append(f"{cwdpath}/{f_name}")
            else:
                # if the user cancel the select dialog I have to asign False
                # or the fileNames will be undefined and the program will crash
                fileNames = False

        # start the adding name(s) to the table
        if fileNames:
            # enable the clear_btn
            self.ui.clear_btn.setEnabled(True)

            # start tacking name by name from the fileNames list
            for name in fileNames:

                # check if the file has added before or not
                duplicate = False
                if self.ui.tableWidget.rowCount():
                    for row in range(self.ui.tableWidget.rowCount()):
                        if name == self.ui.tableWidget.item(row, 3).text():
                            duplicate = True
                            msginfo_lst = [QMessageBox.Warning, "Duplicate Warning",
                                           f"The {QFileInfo(name).fileName()} is in your list!!",
                                           f"{QFileInfo(name).fileName()} will not be added to your list."]
                            msgbox_dailog_mth(msginfo_lst)
                            break

                # adding the name to the table if it not there before
                if not duplicate:

                    # set the 3 var for each column. the name, date, and type
                    fileName = QFileInfo(name).fileName()
                    modificationTime = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(name)))
                    # see if the name is folder or file
                    if os.path.isfile(name):
                        ext_type = QFileInfo(name).suffix()
                        # if the file has no ext then the type by default is 'File'
                        if not ext_type:
                            ext_type = "File"
                    else:
                        ext_type = "Folder"

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
                    if ext_type == "Folder":
                        self.ui.tableWidget.item(row_position, 0).setCheckState(Qt.Unchecked)
                        self.ui.tableWidget.item(row_position, 0).setForeground(Qt.blue)
                    else:
                        self.ui.tableWidget.item(row_position, 0).setCheckState(Qt.Checked)

                    self.ui.tableWidget.item(row_position, 0).setFlags(
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
                if not name:
                    name = ext
                    ext = ""
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
                if ext:
                    item = QtGui.QStandardItem(f"{name}.{ext}")
                else:
                    item = QtGui.QStandardItem(f"{name}{ext}")

                # check if this name is duplicated or not
                # TODO: if the name is duplicated but it's from differnet path
                #  then just change the color to skyblue or green
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
            self.ui.erase_btn.setEnabled(False)
        elif total_row > 0:
            self.ui.rename_btn.setEnabled(True)
            self.ui.addpreset_btn.setEnabled(True)

        # enable only the erase_btn if the user input anything in any field
        if userfield_len > 0:
            self.ui.erase_btn.setEnabled(True)

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
                    msginfo_lst = [QMessageBox.Warning, "Duplicate Warning",
                                   "You Have One Or More Duplicated Name!!",
                                   "Please Check Your Name(s) List, and Try Again."]
                    msgbox_dailog_mth(msginfo_lst)
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

                    # save the userinput in history.pset file
                    self.addpreset_history_mth("history.pset")

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

        # to clear all the input fields
        self.set_fields_mth("erase")        

        # disable the clear_btn
        self.ui.clear_btn.setEnabled(False)

    def set_fields_mth(self, set_lst):
        # make 7 empty space by " "*6, then split them by " "
        if set_lst == "erase":
            set_lst = (" " * 6).split(" ")
            
            # set the cobox to there default value
            self.ui.preset_cobox.setCurrentIndex(0)
            self.ui.log_cobox.setCurrentIndex(0)

        # set the preset
        self.ui.name_LE.setText(set_lst[0])
        self.ui.serial_LE.setText(set_lst[1])
        self.ui.ext_LE.setText(set_lst[2])
        self.ui.order_LE.setText(set_lst[3])
        self.ui.fansub_LE.setText(set_lst[4])
        self.ui.delay_LE.setText(set_lst[5])
        self.ui.lang_cobox.setCurrentText(set_lst[6])

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

    def addpreset_history_mth(self, file_name):
        # call the userinput_mth to collecate the user input information
        userinput_info_lst = self.userinput_mth()

        # the full date
        full_date = datetime.datetime.now()
        # if there is no text in the name_LE I wll creat a default name by the date
        if file_name == "userinput.pset":
            default_name = userinput_info_lst[0] if len(userinput_info_lst[0]) != 0 else "Preset " + full_date.strftime(
                "%d-%m-%y_%H-%M")
        else:
            # I will allways create preset name by the date for the history.pset names
            default_name = "Preset " + full_date.strftime("%d-%m-%y_%H-%M")

        # write the userinput information in the userinput.pset file
        try:
            with open(f"{self.tmp_path}{file_name}", "r+") as preset:
                pset_lst = preset.readlines()
                # set the preset limit to 10 preset only
                limit_reach = False
                if len(pset_lst) < 10:
                    # if the user want to save the preset a QDailoginput will ask him for the name
                    if file_name == "userinput.pset":
                        preset_name = self.get_preset_name_mth(default_name)
                        if preset_name:
                            preset_dict = {"Preset Name": preset_name, "Preset info": userinput_info_lst}
                    else:
                        preset_dict = {"Preset Name": default_name, "Preset info": userinput_info_lst}

                    # this will rise error if the above if didn't defined the preset_dict
                    preset.write(str(preset_dict) + "\n")
                else:
                    # update history.pset by deleting the first preset and shift all the lines up then add the new preset
                    if file_name == "history.pset":
                        del pset_lst[0]  # delete the first line
                        preset.seek(0)  # start from the first line
                        preset.truncate()  # clear the file
                        preset.writelines(pset_lst)  # add the rest of the lines to the file from the top
                        # insert the new line in the bottom
                        preset_dict = {"Preset Name": default_name, "Preset info": userinput_info_lst}
                        preset.write(str(preset_dict) + "\n")
                    else:
                        # show msg wrning that the user reach the preset limits and he/she must delete one or more preset
                        msginfo_lst = [QMessageBox.Warning, "Add Preset Warning",
                                       "Preset Limite Reach",
                                       "you need to delete one or more from your Preset(s) Droplist"]
                        msgbox_dailog_mth(msginfo_lst)
                        limit_reach = True
        except UnboundLocalError:
            preset.close()
        else:
            if not limit_reach:
                self.preset_history_cobox_mth(file_name)

    def preset_history_cobox_mth(self, file_name):
        try:
            # first know which combobox is called and save it name in cobox_name var
            cobox_name = self.ui.preset_cobox if file_name == "userinput.pset" else self.ui.log_cobox

            # clear the combobox before add the new preset, from down to up
            for i in range(cobox_name.count(), 1, -1):
                cobox_name.removeItem(i)

            # add preset name to the combobox
            with open(f"{self.tmp_path}{file_name}", "r") as preset:
                for i, line in enumerate(preset.readlines()):
                    # the literal_eval() mth from ast is to convert back the text line from str to dict
                    line = ast.literal_eval(line)
                    cobox_name.addItem(line["Preset Name"])

        except FileNotFoundError:
            # only creat the file if it not exists
            with open(f"{self.tmp_path}{file_name}", "x"):
                pass

    def set_preset_mth(self, index):
        # get the name of the combobox from the sender mth
        combobox_name = self.sender().objectName()
        # set the file_name and rest the other cobox to it's default name
        if combobox_name == "preset_cobox":
            file_name = "userinput.pset"
            if index:
                self.ui.log_cobox.setCurrentIndex(0)
        else:
            file_name = "history.pset"
            if index:
                self.ui.preset_cobox.setCurrentIndex(0)

        with open(f"{self.tmp_path}{file_name}", "r") as preset:
            # read the preset file and remove the newline char '\n'
            preset_lst = preset.read().splitlines()
            line = preset_lst[index - 1]
            # the literal_eval() mth from ast is to convert back the text line from str to dict
            line = ast.literal_eval(line)
            # see if the user select the default name or not
            if index:
                set_lst = line["Preset info"]
                if combobox_name == "preset_cobox":
                    self.ui.x_btn.setEnabled(True)
            else:
                self.ui.x_btn.setEnabled(False)
                set_lst = "erase"

            # set the preset
            self.set_fields_mth(set_lst)

    def del_preset_mth(self):
        print("test")

    def on_customContextMenuRequested(self, pos):
        # TODO: add two contextmenu to select all the rows or unselect all
        #  and maybe select folder name only or select file name only
        #  and see if I can make select files by there exe
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

        # TODO: maybe add warning msgbox before the delete confirm???
        if action == delete_selected_action:
            check_state = QtCore.Qt.Checked
        elif action == delete_unselected_action:
            check_state = QtCore.Qt.Unchecked
        else:
            check_state = None
        
        for index in reversed(range(total_rows)):
            if cell(index, 0).checkState() == check_state:
                row.removeRow(index)

        # update the listview after the delete
        self.preview_mth()

        # disable the clear_btn if there is no rows
        if self.ui.tableWidget.rowCount() == 0:
            self.ui.clear_btn.setEnabled(False)

    def get_preset_name_mth(self, preset_name):
        text, okPressed = QInputDialog.getText(self, "Get Preset Name", "Your Preset name:", QLineEdit.Normal,
                                               preset_name)
        if okPressed and text != '':
            return text
        else:
            return False

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
