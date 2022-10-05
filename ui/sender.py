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

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QPixmap

from ui.raw.ui_sender import Ui_Sender

from src.mail import MailSMTP
from src.smtp import SMTPHost, SMTPPort
from src.config import mail_login, mail_password


class Sender(QMainWindow, Ui_Sender):
    def __init__(self):
        super(Sender, self).__init__()
        self.setupUi(self)

        # It's a declaration of data to the letter header
        self.whoms: str = ""
        self.subject: str = ""

        # It's a tracking of button clicks in the window
        self.toolApplyWhom.clicked.connect(lambda: self.toolApplyWhom_Clicked())
        self.toolApplySubject.clicked.connect(lambda: self.toolApplySubject_Clicked())
        self.toolAddImage.clicked.connect(lambda: self.toolAddImage_Clicked())
        self.toolResetImage.clicked.connect(lambda: self.toolResetImage_Clicked())
        self.textMessage.textChanged.connect(lambda: self.textMessage_Changed())
        self.buttSend.clicked.connect(lambda: self.buttSend_Clicked())

    def toolApplyWhom_Clicked(self):
        """
        It checks if the text in the line edit is empty, if it is, it displays a warning message box, if not, it disables
        the line edit
        :return: The return value is the value of the None if no expression was evaluated.
        """
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
        """
        It checks if the subject line is empty, if it is, it displays a warning message, if it isn't, it disables the
        subject line
        :return: The return value is the value of the None if no expression was evaluated.
        """
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
        """
        If the lineWhom and lineSubject are not enabled, then the textMessage is enabled and the textMessage_Changed
        function is called
        """
        if not self.lineWhom.isEnabled() and not self.lineSubject.isEnabled():
            self.textMessage.setEnabled(True)
            self.textMessage_Changed()
        else:
            self.textMessage.setEnabled(False)
            if self.buttSend.isEnabled():
                self.buttSend.setEnabled(False)

    def toolAddImage_Clicked(self):
        """
        It opens a file dialog, sets the text of the imageAddress line edit to the path of the selected file, and
        enables/disables the appropriate buttons
        """
        self.imageAddress.setText(QFileDialog.getOpenFileName(self, caption="Selecting an image", directory=str(QDir.homePath()), filter="Images (*.png *.xpm *.jpg)")[0])
        self.toolAddImage.setEnabled(False)
        self.toolResetImage.setEnabled(True)

        # It's just a preview of the image
        pixmap = QPixmap(self.imageAddress.text())
        pixmap = pixmap.scaled(200, 200)
        self.imagePixmap.setPixmap(pixmap)

    def toolResetImage_Clicked(self):
        """
        It resets the image address text box and enables the add image button.
        """
        self.imageAddress.setText("")
        self.toolAddImage.setEnabled(True)
        self.toolResetImage.setEnabled(False)

        # Removing image from preview
        self.imagePixmap.clear()

    def textMessage_Changed(self):
        """
        If the text box is not empty and the send button is disabled, enable the send button. If the text box is empty and
        the send button is enabled, disable the send button
        """
        if not self.textMessage.toPlainText() == "" and not self.buttSend.isEnabled():
            self.buttSend.setEnabled(True)
        if self.textMessage.toPlainText() == "" and self.buttSend.isEnabled():
            self.buttSend.setEnabled(False)

    def buttSend_Clicked(self):
        """
        It sends an email with an image attachment using the Gmail SMTP server
        """
        gmail = MailSMTP(SMTPHost.gmail.value, SMTPPort.gmail.value)
        gmail.server_login(mail_login, mail_password, self.checkAnonymous.isChecked())
        gmail.create_message(self.lineWhom.text().split(', '), self.lineSubject.text(), self.textMessage.toPlainText())
        if self.imageAddress.text() != "":
            gmail.add_image(self.imageAddress.text())
        try:
            gmail.send()
        except TimeoutError as error:
            gmail.close()
            self.TimeoutError_Message(error)
        except AttributeError as error:
            gmail.close()
            self.AttributeError_Message(error)
        else:
            gmail.close()
            self.Close_Message()

    def TimeoutError_Message(self, error: TimeoutError):
        """
        If the host does not support anonymous mailing and it was not possible to send the letter - a
        window is displayed with a request to repeat the operation (anonymous sending is automatically
        disabled and blocked)
        """
        self.checkAnonymous.setChecked(False)
        self.checkAnonymous.setEnabled(False)
        inform = QMessageBox()
        inform.setText(str(error))
        inform.setInformativeText("Try again")
        inform.setIcon(QMessageBox.Icon.Information)
        inform.setStandardButtons(QMessageBox.StandardButton.Ok)
        ret: int = inform.exec()
        match ret:
            case QMessageBox.StandardButton.Ok:
                return

    def AttributeError_Message(self, error: AttributeError):
        """
        If sending the letter failed because the recipient addresses were entered incorrectly -
        a window is displayed asking to correct the errors in the addresses
        """
        warning = QMessageBox()
        warning.setText(str(error))
        warning.setInformativeText("Try again: Please enter a valid recipient address")
        warning.setIcon(QMessageBox.Icon.Warning)
        warning.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort)
        ret: int = warning.exec()
        match ret:
            case QMessageBox.StandardButton.Ok:
                return
            case QMessageBox.StandardButton.Abort:
                self.close()
                return

    def Close_Message(self):
        """
        It's just a notification about the successful sending of the letter
        """
        res = QMessageBox()
        res.setText("The letter has been sent")
        res.setIcon(QMessageBox.Icon.Information)
        res.setStandardButtons(QMessageBox.StandardButton.Ok)
        ret: int = res.exec()
        match ret:
            case QMessageBox.StandardButton.Ok:
                self.close()
