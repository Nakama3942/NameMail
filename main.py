import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    while True:
        app = QApplication(sys.argv)
        try:
            with open('init/config.ini'):
                pass
        except IOError:
            from ui.logindialog import LoginDialog
            login = LoginDialog()
            login.show()
            result: int = login.exec()
            match result:
                case QtWidgets.QDialogButtonBox.StandardButton.Abort.value:
                    sys.exit()
                case QtWidgets.QDialogButtonBox.StandardButton.Apply.value:
                    pass  # Можна продовжувати роботу
                case _:
                    sys.exit()

        from ui.namemail import NameMail
        ui = NameMail()
        ui.show()
        app.exec()
        if not ui.REBOOT:
            break
        app = None

    sys.exit()
