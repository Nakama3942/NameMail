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
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.raw.ui_reviewer import Ui_Reviewer

from src.mail import *
from src.smtp import SMTPHost
from src.config import mail, password


class Reviewer(QMainWindow, Ui_Reviewer):
    def __init__(self, number_mail: int, message_from: str, message_subject: str):
        super(Reviewer, self).__init__()
        self.setupUi(self)

        get_mail = MailIMAP(SMTPHost.gmail.value)
        get_mail.server_login(mail, password)
        part_message = get_mail.get_message(number_mail)
        message: str = ""
        if len(part_message) > 1:
            part_message = part_message[1:]
        for item in part_message:
            message += item
        self.labelFrom.setText(message_from)
        self.labelSubject.setText(message_subject)
        self.textMail.setHtml(str(message))
        get_mail.close()
