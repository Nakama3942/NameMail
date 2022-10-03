import configparser

config = configparser.ConfigParser()
config.read("init/config.ini")

"""Assigning the value of the key "mail_login" in the section "Mail" to the variable "mail_login"."""
mail_login = config["Mail"]["mail_login"]

"""Assigning the value of the key "mail_password" in the section "Mail" to the variable "mail_password"."""
mail_password = config["Mail"]["mail_password"]
