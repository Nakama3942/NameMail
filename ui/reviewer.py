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
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QIcon

from ui.raw.ui_reviewer import Ui_Reviewer

from src.mail import *
from src.smtp import SMTPHost
from src.config import mail_login, mail_password


class Reviewer(QMainWindow, Ui_Reviewer):
    def __init__(self, number_mail: int, message_from: str, message_data: str, message_subject: str):
        super(Reviewer, self).__init__()
        self.setupUi(self)

        # Icon initialization
        QDir.addSearchPath('icons', 'icons/')
        self.setWindowIcon(QIcon('icons:Review_Icon.png'))

        # Connecting to the server and reads the full message
        get_mail = MailIMAP(SMTPHost.gmail.value)
        get_mail.server_login(mail_login, mail_password)
        get_mail.get_list()
        get_mail.get_message(number_mail)

        # Forming a message
        message: str = ""
        if len(get_mail.message) > 1:
            get_mail.message = get_mail.message[1:]
        for item in get_mail.message:
            message += item

        # Displaying the message
        self.labelFrom.setText(message_from)
        self.labelData.setText(message_data)
        self.labelSubject.setText(message_subject)
        self.textMail.setHtml(str(message))

        # Closing the connection with the server
        get_mail.close()
