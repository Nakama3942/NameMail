import enum


class SMTPHost(enum.Enum):
    gmail = 'smtp.gmail.com'
    mail = 'smtp.mail.ru'
    freemail = 'freemail.ukr.net'


class SMTPPort(enum.Enum):
    gmail = 465
    mail = 465
    freemail = 993
