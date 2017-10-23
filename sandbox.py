from chamber import Chamber
import os, sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chamber()
    sys.exit(app.exec_())


