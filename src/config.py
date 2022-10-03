import configparser

config = configparser.ConfigParser()
config.read("init/config.ini")

mail_login = config["Mail"]["mail_login"]
mail_password = config["Mail"]["mail_password"]
