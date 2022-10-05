# Form implementation generated from reading ui file 'NameMail.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_NameMail(object):
    def setupUi(self, NameMail):
        NameMail.setObjectName("NameMail")
        NameMail.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(NameMail)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttSend = QtWidgets.QPushButton(self.centralwidget)
        self.buttSend.setMinimumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttSend.setFont(font)
        self.buttSend.setObjectName("buttSend")
        self.horizontalLayout.addWidget(self.buttSend)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listLetters = QtWidgets.QListWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listLetters.setFont(font)
        self.listLetters.setGridSize(QtCore.QSize(0, 100))
        self.listLetters.setBatchSize(100)
        self.listLetters.setObjectName("listLetters")
        self.verticalLayout.addWidget(self.listLetters)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        NameMail.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NameMail)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menureset = QtWidgets.QMenu(self.menubar)
        self.menureset.setEnabled(False)
        self.menureset.setObjectName("menureset")
        NameMail.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NameMail)
        self.statusbar.setObjectName("statusbar")
        NameMail.setStatusBar(self.statusbar)
        self.actionRelogin = QtGui.QAction(NameMail)
        self.actionRelogin.setObjectName("actionRelogin")
        self.actionRedownload = QtGui.QAction(NameMail)
        self.actionRedownload.setObjectName("actionRedownload")
        self.menureset.addAction(self.actionRelogin)
        self.menureset.addAction(self.actionRedownload)
        self.menubar.addAction(self.menureset.menuAction())

        self.retranslateUi(NameMail)
        QtCore.QMetaObject.connectSlotsByName(NameMail)

    def retranslateUi(self, NameMail):
        _translate = QtCore.QCoreApplication.translate
        NameMail.setWindowTitle(_translate("NameMail", "NameMail"))
        self.buttSend.setText(_translate("NameMail", "To write a letter"))
        self.menureset.setTitle(_translate("NameMail", "reset"))
        self.actionRelogin.setText(_translate("NameMail", "Relogin"))
        self.actionRedownload.setText(_translate("NameMail", "Redownload"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NameMail = QtWidgets.QMainWindow()
    ui = Ui_NameMail()
    ui.setupUi(NameMail)
    NameMail.show()
    sys.exit(app.exec())
