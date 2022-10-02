import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Origin source:
#   https://www.youtube.com/watch?v=mWZYn5I_jkY
#   https://codehandbook.org/how-to-read-email-from-gmail-using-python/
#   (VPN:) https://www.dmosk.ru/instruktions.php?object=python-mail


class MailSMTP:
    def __init__(self, mail_host: str, mail_port: int):
        self.server = smtplib.SMTP_SSL(mail_host, mail_port)
        self.mail: str = ""
        self.password: str = ""
        self.anonymous: bool = False
        self.msg: MIMEMultipart = MIMEMultipart()
        self.to_mail: list[str] = []

    def server_login(self, mail_address: str, mail_password: str, anonymous: bool = False):
        self.mail = mail_address
        self.password = mail_password
        self.server.ehlo()
        if anonymous:
            self.anonymous = anonymous
        else:
            self.server.login(self.mail, self.password)

    def create_message(self, to_address: list[str], mail_subject: str, message: str):
        self.to_mail = to_address
        # Формування листа
        self.msg['From'] = self.mail.split('@')[0]
        self.msg['To'] = ', '.join(self.to_mail)
        self.msg['Subject'] = mail_subject
        self.msg.attach(MIMEText(message, 'plain'))

    def add_image(self, image_name: str):
        # Додання зображення
        attacment = open(image_name, 'rb')

        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attacment.read())

        email.encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={image_name}')
        self.msg.attach(p)

    def send(self):
        # Відправка листа
        text = self.msg.as_string()
        try:
            self.server.sendmail(self.mail, self.to_mail, text)
        except smtplib.SMTPSenderRefused:
            if self.anonymous:
                raise TimeoutError("The server does not support the ability to send anonymous messages!")

    def close(self):
        self.server.close()


class MailIMAP:
    def __init__(self, mail_host: str):
        self.server = imaplib.IMAP4_SSL(mail_host)
        self.mail: str = ""
        self.password: str = ""
        self.current_number_message: int = 0
        self.messages: list[email.message] = []
        self.message: list[str] = []

    def server_login(self, mail_address: str, mail_password: str):
        self.mail = mail_address
        self.password = mail_password
        self.server.login(self.mail, self.password)
        self.server.select('INBOX')

    def get_messages(self) -> list[email.message]:
        _, data = self.server.search(None, 'ALL')
        id_list = data[0].split()

        for item in range(int(id_list[-1]), int(id_list[0]), -1)[:20]:
            self.current_number_message += 1
            data = self.server.fetch(str(item), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    message = email.message_from_string(str(arr[1], 'utf-8'))
                    self.messages.append(message)

        return self.messages

    def get_message(self, number_message: int) -> list[str]:
        _, data = self.server.search(None, 'ALL')
        id_list = data[0].split()
        select_message = id_list[len(id_list) - number_message - 1]

        _, data = self.server.fetch(select_message, '(RFC822)')
        raw_email_string = data[0][1].decode('utf-8')

        email_message = email.message_from_string(raw_email_string)

        if email_message.is_multipart():
            for payload in email_message.get_payload():
                self.message.append(payload.get_payload(decode=True).decode('utf-8'))
        else:
            self.message.append(email_message.get_payload(decode=True).decode('utf-8'))

        return self.message

    def close(self):
        self.server.close()
