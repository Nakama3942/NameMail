import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from config import *


class Mail:
    def __init__(self, mail_host: str = 'smtp.gmail.com', mail_port: int = 465):
        self.server = smtplib.SMTP_SSL(mail_host, mail_port)

    def server_login(self):
        self.server.ehlo()
        self.server.login(mail, password)

    def messaging(self):
        # Формування листа
        msg = MIMEMultipart()
        msg['From'] = 'Nakama3942'
        msg['To'] = 'valentynkalynovskyi@gmail.com'
        msg['Subject'] = 'Just a test'

        with open('message.txt', 'r') as file:
            message = file.read()

        msg.attach(MIMEText(message, 'plain'))

        # Додання зображення
        image_name = 'image.jpg'
        attacment = open(image_name, 'rb')

        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attacment.read())

        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={image_name}')
        msg.attach(p)

        # Відправка листа
        text = msg.as_string()
        self.server.sendmail(mail, 'valentynkalynovskyi@gmail.com', text)
