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

"""
Origin source:
    https://www.pythonguis.com/tutorials/first-steps-qt-creator/
"""

from threading import Thread
import pickle
import os

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread, pyqtSignal

from ui.raw.ui_namemail import Ui_NameMail
from ui.reviewer import Reviewer
from ui.sender import Sender

from src.mail import *
from src.smtp import SMTPHost
from src.config import mail_login, mail_password


# It's a QThread that emits a signal of downloads letter
class ProgressThread(QThread):
    update = pyqtSignal(int, int)

    def __init__(self, get_mail: MailIMAP):
        super(ProgressThread, self).__init__()
        self.get_mail = get_mail

    def run(self):
        """
        This is a function that gives a signal to update the progress bar in the GUI
        """
        count_mails = len(self.get_mail.id_list) - 1
        current = len(self.get_mail.messages)
        while current <= count_mails:
            if current < len(self.get_mail.messages):
                self.update.emit(current := len(self.get_mail.messages), count_mails)
            if current == count_mails:
                break


class NameMail(QMainWindow, Ui_NameMail):
    def __init__(self):
        super(NameMail, self).__init__()
        self.setupUi(self)
        self.REBOOT: bool = False

        # It's a declaration of other windows of the program
        self.reviewer = None
        self.sender = None

        # It's a declaration of lists of data headers of letters
        self.message_from: list[str] = []
        self.message_date: list[str] = []
        self.message_subject: list[str] = []

        # Formation of the string progress of uploading letters to the status bar
        self.progressbar = QtWidgets.QProgressBar()
        self.status = QtWidgets.QLabel()
        self.status.setText("Hello ＼(＾▽＾)／")
        self.statusbar.addWidget(self.progressbar)
        self.statusbar.addWidget(self.status)

        # It's a tracking of button clicks in the window
        self.buttSend.released.connect(lambda: self.buttSend_Released())
        self.listLetters.activated.connect(lambda: self.listLetters_Activated(self.listLetters.currentRow()))
        self.actionRelogin.triggered.connect(lambda: self.actionRelogin_Triggered())
        self.actionRedownload.triggered.connect(lambda: self.actionRedownload_Triggered())

        # It's a downloading of messages in a separate thread
        get_mail = MailIMAP(SMTPHost.gmail.value)
        mail_thread = Thread(target=self.download_message, args=(get_mail,), daemon=True)
        mail_thread.start()

    def download_message(self, get_mail: MailIMAP):
        try:
            # It's a reading of downloaded messages from a file
            with open("init/data.msg", "rb") as data:
                get_mail.messages = pickle.load(data)
            self.progressbar.setMaximum(len(get_mail.messages))
            self.progressbar.setValue(len(get_mail.messages))
            self.status.setText("Mail opened <(￣︶￣)>")
        except IOError:
            # If it is not possible to read the messages from the file, started download them from
            # the server and saving to the file.
            get_mail.server_login(mail_login, mail_password)
            get_mail.get_list()

            progress_thread = ProgressThread(get_mail)
            progress_thread.start()
            progress_thread.update.connect(self.update_status_bar)

            get_mail.get_messages()
            get_mail.close()

            with open("init/data.msg", "wb") as data:
                pickle.dump(get_mail.messages, data)
            self.status.setText("Mail downloaded ＼(≧▽≦)／")

        self.set_messages_to_list(get_mail)

    def set_messages_to_list(self, get_mail: MailIMAP):
        """
        It displays downloaded messages
        """
        count = 0
        for item in get_mail.messages:
            count += 1
            item_from = str(email.header.make_header(email.header.decode_header(item['from'])))
            item_date = str(email.header.make_header(email.header.decode_header(item['date'])))
            item_subject = str(email.header.make_header(email.header.decode_header(item['subject'])))
            self.listLetters.addItem(QtWidgets.QListWidgetItem(f"Message #{count}\n"
                                                               f"From : {item_from}\n"
                                                               f"Data : {item_date}\n"
                                                               f"Subject : {item_subject}"))
            self.message_from.append(item_from)
            self.message_date.append(item_date)
            self.message_subject.append(item_subject)
        self.menureset.setEnabled(True)

    def update_status_bar(self, current: int, max: int):
        """
        If ProgressThread reports that a new letter has been loaded - display the current progress
        """
        self.progressbar.setMaximum(max)
        self.progressbar.setValue(current)
        self.status.setText(f"Mining bitcoins: {current} out of {max} ¯\_(ツ)_/¯")

    def buttSend_Released(self):
        """
        It's a displaying of the window of writing a letter
        """
        self.sender = Sender()
        self.sender.show()

    def listLetters_Activated(self, number_item: int):
        """
        It's a displaying of the window with the full content of the letter
        """
        self.reviewer = Reviewer(number_item,
                                 self.message_from[number_item],
                                 self.message_date[number_item],
                                 self.message_subject[number_item])
        self.reviewer.show()

    def actionRelogin_Triggered(self):
        """
        It's a deleting of all files and restarting the program
        """
        os.remove("init/config.ini")
        self.actionRedownload_Triggered()

    def actionRedownload_Triggered(self):
        """
        It's a deleting of the file with messages and restarting the program
        """
        os.remove("init/data.msg")
        self.REBOOT = True
        self.close()
