import sys
# from mail import MailSMTP, MailIMAP
# from smtp import *
# from config import *
from ui.namemail import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = NameMail()
    ui.show()
    sys.exit(app.exec())

# def TestSMTP():
#     with open('message.txt', 'r') as file:
#         message = file.read()
#
#     gmail = MailSMTP(SMTPHost.gmail.value, SMTPPort.gmail.value)
#     gmail.server_login(mail, password)
#     gmail.create_message(['valentynkalynovskyi@gmail.com',
#                           'dzonile.f.g.i@gmail.com',
#                           'kalinovskijvalentin@gmail.com'],
#                          'Just a test',
#                          message)
#     gmail.add_image('image.jpg')
#     gmail.send()
#     gmail.close()
#
#
# def TestIMAP():
#     imail = MailIMAP(SMTPHost.gmail.value)
#     imail.server_login(mail, password)
#     imail.get_message()
#     imail.close()
