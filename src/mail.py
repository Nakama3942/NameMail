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
    https://www.youtube.com/watch?v=mWZYn5I_jkY
    https://codehandbook.org/how-to-read-email-from-gmail-using-python/
    (VPN:) https://www.dmosk.ru/instruktions.php?object=python-mail
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class MailSMTP:
    """
    This class is used to send emails using SMTP
    """
    def __init__(self, mail_host: str, mail_port: int):
        """
        This function initializes the class with the mail host and port

        :param mail_host: The host of the mail server
        :type mail_host: str
        :param mail_port: The port to connect to the mail server
        :type mail_port: int
        """
        self.server = smtplib.SMTP_SSL(mail_host, mail_port)
        self.mail: str = ""
        self.password: str = ""
        self.anonymous: bool = False
        self.msg: MIMEMultipart = MIMEMultipart()
        self.to_mail: list[str] = []

    def server_login(self, mail_address: str, mail_password: str, anonymous: bool = False):
        """
        The function takes in a mail address, a password, and a boolean value. If the boolean value is true, the function
        will log in anonymously. If the boolean value is false, the function will log in with the mail address and password

        :param mail_address: The email address you want to send the email from
        :type mail_address: str
        :param mail_password: The password of the mail account you want to send the mail from
        :type mail_password: str
        :param anonymous: If you want to send an anonymous email, set this to True, defaults to False
        :type anonymous: bool (optional)
        """
        self.mail = mail_address
        self.password = mail_password
        self.server.ehlo()
        if anonymous:
            self.anonymous = anonymous
        else:
            self.server.login(self.mail, self.password)

    def create_message(self, to_address: list[str], mail_subject: str, message: str):
        """
        The function takes in three arguments, to_address, mail_subject, and message.
        It then sets the to_mail attribute to the to_address argument.
        It then sets the msg['From'] attribute to the first part of the mail attribute,
        which is the username. It then sets the msg['To'] attribute to a comma separated
        string of the to_mail attribute. It then sets the msg['Subject'] attribute to the
        mail_subject argument. It then attaches a MIMEText object to the msg attribute.
        The MIMEText object takes in two arguments, message and 'plain'

        :param to_address: The emails address of the recipient
        :type to_address: list[str]
        :param mail_subject: The subject of the email
        :type mail_subject: str
        :param message: The message to be sent
        :type message: str
        """
        self.to_mail = to_address
        self.msg['From'] = self.mail.split('@')[0]
        self.msg['To'] = ', '.join(self.to_mail)
        self.msg['Subject'] = mail_subject
        self.msg.attach(MIMEText(message, 'plain'))

    def add_image(self, image_name: str):
        """
        We open the image, create a MIMEBase object, set the payload, encode it, add a header, and attach it to the message

        :param image_name: The name of the image file you want to attach
        :type image_name: str
        """
        attacment = open(image_name, 'rb')

        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attacment.read())

        email.encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={image_name}')
        self.msg.attach(p)

    def send(self):
        """
        The function sends the message to the recipient
        """
        text = self.msg.as_string()
        try:
            self.server.sendmail(self.mail, self.to_mail, text)
        except smtplib.SMTPSenderRefused:
            if self.anonymous:
                raise TimeoutError("The server does not support the ability to send anonymous messages!")
        except smtplib.SMTPRecipientsRefused:
            raise AttributeError("Invalid recipient address: address does not exist!")

    def close(self):
        """
        The function closes the server
        """
        self.server.close()


class MailIMAP:
    """
    This class is used to connect to an IMAP server and retrieve emails
    """
    def __init__(self, mail_host: str):
        """
        This function initializes the class with the mail host and sets the server to the mail host

        :param mail_host: The host of the email server
        :type mail_host: str
        """
        self.server = imaplib.IMAP4_SSL(mail_host)
        self.mail: str = ""
        self.password: str = ""
        self.id_list = None
        self.messages: list[email.message] = []
        self.message: list[str] = []

    def server_login(self, mail_address: str, mail_password: str):
        """
        The function takes in a mail address and password, and logs into the server using the mail address and password

        :param mail_address: The email address you want to download the emails from
        :type mail_address: str
        :param mail_password: The password for the email account you're using
        :type mail_password: str
        """
        self.mail = mail_address
        self.password = mail_password
        self.server.login(self.mail, self.password)
        self.server.select('INBOX')

    def get_list(self):
        """
        It searches the inbox for all messages and returns a list of their IDs
        """
        _, data = self.server.search(None, 'ALL')
        self.id_list = data[0].split()

    def get_messages(self):
        """
        It takes the last and first id's from the list of id's, and then loops through the range of those two id's, fetching
        the message from the server and appending it to the messages list.
        """
        for item in range(int(self.id_list[-1]), int(self.id_list[0]), -1):
            data = self.server.fetch(str(item), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    message = email.message_from_string(str(arr[1], 'utf-8'))
                    self.messages.append(message)

    def get_message(self, number_message: int):
        """
        It takes the number of the message you want to read, finds the message ID, fetches the message, decodes it, and
        assembles the parts into a single message

        :param number_message: The number of the message you want to get
        :type number_message: int
        """
        select_message = self.id_list[len(self.id_list) - number_message - 1]

        _, data = self.server.fetch(select_message, '(RFC822)')
        raw_email_string = data[0][1].decode('utf-8')

        email_message = email.message_from_string(raw_email_string)

        if email_message.is_multipart():
            for payload in email_message.get_payload():
                self.message.append(payload.get_payload(decode=True).decode('utf-8'))
        else:
            self.message.append(email_message.get_payload(decode=True).decode('utf-8'))

    def close(self):
        """
        The function closes the server
        """
        self.server.close()
