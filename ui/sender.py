#  Copyright © 2022 Kalynovsky Valentin. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from ui.raw.ui_sender import Ui_Sender

from src.mail import MailSMTP
from src.smtp import SMTPHost, SMTPPort
from src.config import mail, password


class Sender(QMainWindow, Ui_Sender):
    def __init__(self):
        super(Sender, self).__init__()
        self.setupUi(self)

        self.whoms: str = ""
        self.subject: str = ""

        # Об'єданння графічних елементів зі слотами
        self.toolApplyWhom.clicked.connect(lambda: self.toolApplyWhom_Clicked())
        self.toolApplySubject.clicked.connect(lambda: self.toolApplySubject_Clicked())
        self.toolAddImage.clicked.connect(lambda: self.toolAddImage_Clicked())
        self.toolResetImage.clicked.connect(lambda: self.toolResetImage_Clicked())
        self.textMessage.textChanged.connect(lambda: self.textMessage_Changed())
        self.buttSend.clicked.connect(lambda: self.buttSend_Clicked())

    def toolApplyWhom_Clicked(self):
        if self.lineWhom.text() == "":
            warning = QMessageBox()
            warning.setText("Address missing")
            warning.setInformativeText("Enter at one least the recipient's address!")
            warning.setIcon(QMessageBox.Icon.Critical)
            warning.setStandardButtons(QMessageBox.StandardButton.Cancel)
            ret: int = warning.exec()
            match ret:
                case QMessageBox.StandardButton.Cancel:
                    self.toolApplyWhom.setChecked(False)
                    return
        self.whoms = self.lineWhom.text()
        if self.lineWhom.isEnabled():
            self.lineWhom.setEnabled(False)
        else:
            self.lineWhom.setEnabled(True)
        self.checks_applies()

    def toolApplySubject_Clicked(self):
        if self.lineSubject.text() == "":
            warning = QMessageBox()
            warning.setText("Subject missing")
            warning.setInformativeText("Enter the subject of the letter!")
            warning.setIcon(QMessageBox.Icon.Warning)
            warning.setStandardButtons(QMessageBox.StandardButton.Ok)
            ret: int = warning.exec()
            match ret:
                case QMessageBox.StandardButton.Ok:
                    self.toolApplySubject.setChecked(False)
                    return
        self.subject = self.lineSubject.text()
        if self.lineSubject.isEnabled():
            self.lineSubject.setEnabled(False)
        else:
            self.lineSubject.setEnabled(True)
        self.checks_applies()

    def checks_applies(self):
        if not self.lineWhom.isEnabled() and not self.lineSubject.isEnabled():
            self.textMessage.setEnabled(True)
            self.textMessage_Changed()
        else:
            self.textMessage.setEnabled(False)
            if self.buttSend.isEnabled():
                self.buttSend.setEnabled(False)

    def toolAddImage_Clicked(self):
        self.imageAddress.setText(QFileDialog.getOpenFileName(self, caption="Selecting an image", filter="Images (*.png *.xpm *.jpg)")[0])
        self.toolAddImage.setEnabled(False)
        self.toolResetImage.setEnabled(True)

    def toolResetImage_Clicked(self):
        self.imageAddress.setText("")
        self.toolAddImage.setEnabled(True)
        self.toolResetImage.setEnabled(False)

    def textMessage_Changed(self):
        if not self.textMessage.toPlainText() == "" and not self.buttSend.isEnabled():
            self.buttSend.setEnabled(True)
        if self.textMessage.toPlainText() == "" and self.buttSend.isEnabled():
            self.buttSend.setEnabled(False)

    def buttSend_Clicked(self):
        gmail = MailSMTP(SMTPHost.gmail.value, SMTPPort.gmail.value)
        gmail.server_login(mail, password)
        gmail.create_message(self.lineWhom.text().split(', '), self.lineSubject.text(), self.textMessage.toPlainText())
        if self.imageAddress.text() != "":
            gmail.add_image(self.imageAddress.text())
        gmail.send()
        gmail.close()

        res = QMessageBox()
        res.setText("The letter has been sent")
        res.setIcon(QMessageBox.Icon.Information)
        res.setStandardButtons(QMessageBox.StandardButton.Ok)
        ret: int = res.exec()
        match ret:
            case QMessageBox.StandardButton.Ok:
                self.close()
