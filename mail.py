import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Origin source: https://www.youtube.com/watch?v=mWZYn5I_jkY


class Mail:
    def __init__(self, mail_host: str, mail_port: int):
        self.server = smtplib.SMTP_SSL(mail_host, mail_port)
        self.mail: str = ""
        self.password: str = ""
        self.msg: MIMEMultipart = MIMEMultipart()
        self.to_mail: str = ""

    def server_login(self, mail_address: str, mail_password: str):
        self.mail = mail_address
        self.password = mail_password
        self.server.ehlo()
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
        self.server.sendmail(self.mail, self.to_mail, text)
