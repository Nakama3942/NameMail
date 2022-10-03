import enum


class SMTPHost(enum.Enum):
    """It's an enumeration of the SMTP hosts"""
    gmail = 'smtp.gmail.com'
    mail = 'smtp.mail.ru'
    freemail = 'freemail.ukr.net'


class SMTPPort(enum.Enum):
    """It's an enumeration of the SMTP ports"""
    gmail = 465
    mail = 465
    freemail = 993
