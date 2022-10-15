#  Copyright © 2022 Kalynovsky Valentin. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

if __name__ == "__main__":
    while True:
        app = QApplication(sys.argv)
        try:
            with open('init/config.ini'):
                pass
        except IOError:
            # If the login file is missing, start the login process
            from ui.logindialog import LoginDialog
            login = LoginDialog()
            login.show()
            result: int = login.exec()
            match result:
                case QtWidgets.QDialogButtonBox.StandardButton.Abort.value:
                    sys.exit()
                case QtWidgets.QDialogButtonBox.StandardButton.Apply.value:
                    pass  # Can continue work
                case _:
                    res = QMessageBox()
                    res.setText("Emergency termination")
                    res.setIcon(QMessageBox.Icon.Information)
                    res.setStandardButtons(QMessageBox.StandardButton.Ok)
                    ret: int = res.exec()
                    match ret:
                        case QMessageBox.StandardButton.Ok:
                            sys.exit()

        from ui.namemail import NameMail
        ui = NameMail()
        ui.show()
        app.exec()
        if not ui.REBOOT:
            break  # If the program did not reset the data, exit the cycle and close the program
        app = None

    sys.exit()
