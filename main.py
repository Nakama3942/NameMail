import sys
from ui.namemail import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = NameMail()
    ui.show()
    sys.exit(app.exec())
