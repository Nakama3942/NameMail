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

from threading import Thread

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.raw.ui_namemail import Ui_NameMail
from ui.reviewer import Reviewer
from ui.sender import Sender

from src.mail import *
from src.smtp import SMTPHost
from src.config import mail_login, mail_password

# Origin source:
#   https://www.pythonguis.com/tutorials/first-steps-qt-creator/


class NameMail(QMainWindow, Ui_NameMail):
    def __init__(self):
        super(NameMail, self).__init__()
        self.setupUi(self)
        self.reviewer = None
        self.sender = None
        self.message_from: list[str] = []
        self.message_subject: list[str] = []

        self.progressbar = QtWidgets.QProgressBar()
        self.statusbar.addWidget(self.progressbar)

        # Об'єданння графічних елементів зі слотами
        self.buttSend.released.connect(lambda: self.buttSend_Released())
        self.listLetters.activated.connect(lambda: self.listLetters_Activated(self.listLetters.currentRow()))

        # Формування списку повідомлень
        get_mail = MailIMAP(SMTPHost.gmail.value)
        mail_thread = Thread(target=self.get_message, args=(get_mail,))
        mail_thread.start()

    def get_message(self, get_mail: MailIMAP):
        get_mail.server_login(mail_login, mail_password)
        get_mail.get_list()
        progres_thread = Thread(target=self.progress_bar_reboot, args=(get_mail,))
        progres_thread.start()
        get_mail.get_messages()
        get_mail.close()

    def progress_bar_reboot(self, get_mail: MailIMAP):
        self.progressbar.setMaximum(len(get_mail.id_list) - 1)
        current_number_of_rocessed_list_id = len(get_mail.messages)
        while current_number_of_rocessed_list_id < len(get_mail.id_list) - 1:
            if current_number_of_rocessed_list_id < len(get_mail.messages):
                self.progressbar.setValue(current_number_of_rocessed_list_id := len(get_mail.messages))

                item_from = str(email.header.make_header(email.header.decode_header(get_mail.messages[-1]['from'])))
                item_subject = str(email.header.make_header(email.header.decode_header(get_mail.messages[-1]['subject'])))
                self.listLetters.addItem(QtWidgets.QListWidgetItem(f"From : {item_from}\nSubject : {item_subject}"))
                self.message_from.append(item_from)
                self.message_subject.append(item_subject)

    def buttSend_Released(self):
        self.sender = Sender()
        self.sender.show()

    def listLetters_Activated(self, number_item: int):
        self.reviewer = Reviewer(number_item, self.message_from[number_item], self.message_subject[number_item])
        self.reviewer.show()
