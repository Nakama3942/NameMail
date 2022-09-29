import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from config import *


def server_login() -> smtplib.SMTP_SSL:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(mail, password)
    return server


def messaging(server: smtplib.SMTP_SSL):
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
    server.sendmail(mail, 'valentynkalynovskyi@gmail.com', text)


if __name__ == "__main__":
    gmail = server_login()
    messaging(gmail)
