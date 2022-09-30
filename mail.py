import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import imaplib
import email


class MailSMTP:
    # Origin source: https://www.youtube.com/watch?v=mWZYn5I_jkY
    def __init__(self, mail_host: str, mail_port: int):
        self.server = smtplib.SMTP_SSL(mail_host, mail_port)
        self.mail: str = ""
        self.password: str = ""
        self.anonymous: bool = False
        self.msg: MIMEMultipart = MIMEMultipart()
        self.to_mail: str = ""

    def server_login(self, mail_address: str, mail_password: str, anonymous: bool = False):
        self.mail = mail_address
        self.password = mail_password
        self.server.ehlo()
        if anonymous:
            self.anonymous = anonymous
        else:
            self.server.login(self.mail, self.password)

    def create_message(self, to_address: str, mail_subject: str, message: str):
        self.to_mail = to_address
        # Формування листа
        self.msg['From'] = self.mail.split('@')[0]
        self.msg['To'] = self.to_mail
        self.msg['Subject'] = mail_subject
        self.msg.attach(MIMEText(message, 'plain'))

    def add_image(self, image_name: str):
        # Додання зображення
        attacment = open(image_name, 'rb')

        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attacment.read())

        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={image_name}')
        self.msg.attach(p)

    def send(self):
        # Відправка листа
        text = self.msg.as_string()
        try:
            self.server.sendmail(self.mail, self.to_mail, text)
            print("The message has been sent.")
        except smtplib.SMTPSenderRefused:
            if self.anonymous:
                print("The server does not support the ability to send anonymous messages!")

    def close(self):
        self.server.quit()


class MailIMAP:
    # Origin source: https://codehandbook.org/how-to-read-email-from-gmail-using-python/
    def __init__(self, mail_host: str):
        self.server = imaplib.IMAP4_SSL(mail_host)
        self.mail: str = ""
        self.password: str = ""
        self.messages: list = []

    def server_login(self, mail_address: str, mail_password: str):
        self.mail = mail_address
        self.password = mail_password
        self.server.login(self.mail, self.password)

    def get_message(self):
        self.server.select('INBOX')

        _, data = self.server.search(None, 'ALL')
        id_list = data[0].split()

        for item in range(int(id_list[-1]), int(id_list[0]), -1):
            data = self.server.fetch(str(item), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    print('From : ' + msg['from'] + '\n')
                    print('Subject : ' + msg['subject'] + '\n')

    def close(self):
        self.server.quit()