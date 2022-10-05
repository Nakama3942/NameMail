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

import os
import configparser

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox

from ui.raw.ui_logindialog import Ui_LoginDialog

from src.mail import MailIMAP
from src.smtp import SMTPHost


class LoginDialog(QDialog, Ui_LoginDialog):
    """
    The LoginDialog class inherits from the QDialog class and the Ui_Dialog class
    """
    def __init__(self):
        """
        Initializes the dialog box class that is displayed if there is no configuration file
        """
        super(LoginDialog, self).__init__()
        self.setupUi(self)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Abort).clicked.connect(lambda: self.buttonBox_Abort_Clicked())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).clicked.connect(lambda: self.buttonBox_Apply_Clicked())

    def buttonBox_Abort_Clicked(self):
        """
        If the user clicks the Abort button, a warning message is displayed and the dialog is closed
        """
        warning = QMessageBox()
        warning.setText("Login canceled")
        warning.setInformativeText("No further work possible...")
        warning.setIcon(QMessageBox.Icon.Critical)
        warning.setStandardButtons(QMessageBox.StandardButton.Ok)
        ret: int = warning.exec()
        match ret:
            case QMessageBox.StandardButton.Ok:
                self.done(QtWidgets.QDialogButtonBox.StandardButton.Abort.value)

    def buttonBox_Apply_Clicked(self):
        """
        It creates a config file with the user's email and password
        """
        get_mail = MailIMAP(SMTPHost.gmail.value)
        try:
            get_mail.server_login(self.lineEmail.text(), self.linePassword.text())
        except Exception:
            warning = QMessageBox()
            warning.setText("Login failed")
            warning.setInformativeText("Incorrect login or password. Try again")
            warning.setIcon(QMessageBox.Icon.Warning)
            warning.setStandardButtons(QMessageBox.StandardButton.Ok)
            ret: int = warning.exec()
            match ret:
                case QMessageBox.StandardButton.Ok:
                    return

        if not os.path.exists('init'):
            os.makedirs('init')
        config = configparser.ConfigParser()
        config.add_section('Mail')
        config.set('Mail', 'mail_login', self.lineEmail.text())
        config.set('Mail', 'mail_password', self.linePassword.text())
        with open('init/config.ini', 'w') as config_file:
            config.write(config_file)

        self.done(QtWidgets.QDialogButtonBox.StandardButton.Apply.value)
