import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        file = open('init/config.ini')
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

    from ui.namemail import NameMail
    ui = NameMail()
    ui.show()
    sys.exit(app.exec())
