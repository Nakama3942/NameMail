from mail import Mail
from smtp import *
from config import *

if __name__ == "__main__":
    with open('message.txt', 'r') as file:
        message = file.read()

    gmail = Mail(SMTPHost.gmail.value, SMTPPort.gmail.value)
    gmail.server_login(mail, password)
    gmail.create_message('valentynkalynovskyi@gmail.com', 'Just a test', message)
    gmail.add_image('image.jpg')
    gmail.send()
