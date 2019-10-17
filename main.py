import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo
from UI.maingui import Ui_Form  # importing our generated file


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
                
        # call the all the btn methods
        self.btn_handler()        

    def btn_handler(self):
        self.ui.addfile_btn.clicked.connect(self.preview_mth)
        #self.ui.preview_btn.clicked.connect(self.preview_mth)

    def addfile_mth(self):
        print(self.sender().text())
        try:            
            # QFileDialog.getOpenFileName(self, [Title], [Directory], "[some filters]")
            # leave the dirctory blank to start the app from the running folder
            fileNames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", "C:\\Users\\H.Ali\\Desktop\\Rename test", "All Filles (*)")
            
            if fileNames:
            	for name in fileNames :
            		fileName = QFileInfo(name).fileName()
            		path = QFileInfo(name).path()
            		#print(path)
            		item = QtWidgets.QListWidgetItem()
            		item.setText(fileName)
            		item.setCheckState(QtCore.Qt.Checked)
            		self.ui.listWidget.addItem(item)
        except OSError:
            pass

    def preview_mth(self):
    	sender_btn = self.sender().text()
    	if sender_btn == "Add File(s)":
    		self.addfile_mth()
    	elif sender_btn == "Add Folder":
    		pass
    	else :
	    	checked_items = []
	    	for index in range(self.ui.listWidget.count()):
	    		if self.ui.listWidget.item(index).checkState() == QtCore.Qt.Checked:
	    			checked_items.append(self.ui.listWidget.item(index).text())

	    	model = QtGui.QStandardItemModel()
	    	self.ui.listView.setModel(model)

	    	for i in checked_items:
	    		item = QtGui.QStandardItem(i)

	    		model.appendRow(item)

    def moveUP(self):
    	currentRow = self.ui.listWidget.currentRow()
    	currentItem = self.ui.listWidget.takeItem(currentRow)
    	self.ui.listWidget.insertItem(currentRow - 1, currentItem)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
