# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\H.Ali\Desktop\python test\Rename\UI\maingui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 690)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.log_cobox = QtWidgets.QComboBox(Form)
        self.log_cobox.setMaxVisibleItems(11)
        self.log_cobox.setObjectName("log_cobox")
        self.log_cobox.addItem("")
        self.horizontalLayout_5.addWidget(self.log_cobox)
        self.addfile_btn = QtWidgets.QPushButton(Form)
        self.addfile_btn.setObjectName("addfile_btn")
        self.horizontalLayout_5.addWidget(self.addfile_btn)
        self.addfolder_btn = QtWidgets.QPushButton(Form)
        self.addfolder_btn.setObjectName("addfolder_btn")
        self.horizontalLayout_5.addWidget(self.addfolder_btn)
        self.preview_btn = QtWidgets.QPushButton(Form)
        self.preview_btn.setObjectName("preview_btn")
        self.horizontalLayout_5.addWidget(self.preview_btn)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name_LE = QtWidgets.QLineEdit(Form)
        self.name_LE.setObjectName("name_LE")
        self.horizontalLayout.addWidget(self.name_LE)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.serial_LE = QtWidgets.QLineEdit(Form)
        self.serial_LE.setMaximumSize(QtCore.QSize(50, 16777215))
        self.serial_LE.setObjectName("serial_LE")
        self.horizontalLayout.addWidget(self.serial_LE)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.ext_LE = QtWidgets.QLineEdit(Form)
        self.ext_LE.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ext_LE.setObjectName("ext_LE")
        self.horizontalLayout.addWidget(self.ext_LE)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.order_LE = QtWidgets.QLineEdit(Form)
        self.order_LE.setMaximumSize(QtCore.QSize(50, 16777215))
        self.order_LE.setObjectName("order_LE")
        self.horizontalLayout_2.addWidget(self.order_LE)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.fansub_LE = QtWidgets.QLineEdit(Form)
        self.fansub_LE.setObjectName("fansub_LE")
        self.horizontalLayout_2.addWidget(self.fansub_LE)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.delay_LE = QtWidgets.QLineEdit(Form)
        self.delay_LE.setMaximumSize(QtCore.QSize(50, 16777215))
        self.delay_LE.setObjectName("delay_LE")
        self.horizontalLayout_2.addWidget(self.delay_LE)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.lang_cobox = QtWidgets.QComboBox(Form)
        self.lang_cobox.setObjectName("lang_cobox")
        self.lang_cobox.addItem("")
        self.lang_cobox.setItemText(0, "")
        self.lang_cobox.addItem("")
        self.lang_cobox.addItem("")
        self.lang_cobox.addItem("")
        self.horizontalLayout_2.addWidget(self.lang_cobox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_8 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.date_chbox = QtWidgets.QCheckBox(Form)
        self.date_chbox.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.date_chbox.setObjectName("date_chbox")
        self.horizontalLayout_3.addWidget(self.date_chbox)
        self.type_chbox = QtWidgets.QCheckBox(Form)
        self.type_chbox.setObjectName("type_chbox")
        self.horizontalLayout_3.addWidget(self.type_chbox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_9 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.listView = QtWidgets.QListView(Form)
        self.listView.setAlternatingRowColors(True)
        self.listView.setObjectName("listView")
        self.verticalLayout_3.addWidget(self.listView)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.rename_btn = QtWidgets.QPushButton(Form)
        self.rename_btn.setObjectName("rename_btn")
        self.horizontalLayout_6.addWidget(self.rename_btn)
        self.unrename_btn = QtWidgets.QPushButton(Form)
        self.unrename_btn.setObjectName("unrename_btn")
        self.horizontalLayout_6.addWidget(self.unrename_btn)
        self.clear_btn = QtWidgets.QPushButton(Form)
        self.clear_btn.setObjectName("clear_btn")
        self.horizontalLayout_6.addWidget(self.clear_btn)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.log_cobox.setItemText(0, _translate("Form", "Log History"))
        self.addfile_btn.setText(_translate("Form", "Add File(s)"))
        self.addfolder_btn.setText(_translate("Form", "Add Folder"))
        self.preview_btn.setText(_translate("Form", "Preview"))
        self.label.setText(_translate("Form", "Name:"))
        self.name_LE.setPlaceholderText(_translate("Form", "File Name ex. My_File"))
        self.label_5.setText(_translate("Form", "Serialize:"))
        self.serial_LE.setPlaceholderText(_translate("Form", "1or01..."))
        self.label_7.setText(_translate("Form", "Ext:"))
        self.ext_LE.setPlaceholderText(_translate("Form", "mkv,exe"))
        self.label_3.setText(_translate("Form", "Order:"))
        self.order_LE.setPlaceholderText(_translate("Form", "01 ..."))
        self.label_2.setText(_translate("Form", "Fan-Sub Team:"))
        self.fansub_LE.setPlaceholderText(_translate("Form", "Fan-Sub Team Name"))
        self.label_4.setText(_translate("Form", "Delay (ms):"))
        self.delay_LE.setPlaceholderText(_translate("Form", "1000"))
        self.label_6.setText(_translate("Form", "Lang:"))
        self.lang_cobox.setItemText(1, _translate("Form", "Ara"))
        self.lang_cobox.setItemText(2, _translate("Form", "Eng"))
        self.lang_cobox.setItemText(3, _translate("Form", "Jap"))
        self.label_8.setText(_translate("Form", "Original Name(s):"))
        self.date_chbox.setText(_translate("Form", "Date"))
        self.type_chbox.setText(_translate("Form", "Type"))
        self.label_9.setText(_translate("Form", "New Name(s):"))
        self.rename_btn.setText(_translate("Form", "Rename"))
        self.unrename_btn.setText(_translate("Form", "UnRename"))
        self.clear_btn.setText(_translate("Form", "Clear Lists"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
