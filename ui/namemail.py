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

from ui.raw.ui_namemail import Ui_NameMail
from ui.reviewer import Reviewer

from src.mail import *
from src.smtp import SMTPHost
from src.config import mail, password

# Origin source:
#   https://www.pythonguis.com/tutorials/first-steps-qt-creator/


class NameMail(QMainWindow, Ui_NameMail):
    def __init__(self):
        super(NameMail, self).__init__()
        self.ui = None
        self.setupUi(self)

        # Об'єданння графічних елементів зі слотами
        self.buttSend.released.connect(lambda: self.buttSend_Released())
        self.listLetters.activated.connect(lambda: self.listLetters_Activated(self.listLetters.currentRow()))

        # Формування списку повідомлень
        get_mail = MailIMAP(SMTPHost.gmail.value)
        get_mail.server_login(mail, password)
        messages = get_mail.get_messages()
        for item in messages:
            self.listLetters.addItem(QtWidgets.QListWidgetItem(f"From : {email.header.make_header(email.header.decode_header(item['from']))}\nSubject : {email.header.make_header(email.header.decode_header(item['subject']))}"))
        get_mail.close()

    def buttSend_Released(self):
        # todo Реалізувати вікно відправлення повідомлення
        print("Not available! 111")

    def listLetters_Activated(self, number_item: int):
        self.ui = Reviewer()
        self.ui.show()
