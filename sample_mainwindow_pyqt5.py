import sys

from PyQt5.QtGui import QFont

# IMPORTANT!!!!!!!!!
# to prevent the "QWidget: Must construct a QApplication before a QWidget" error, you should put the code below
from pyqt_frameless_window import FramelessDialog, FramelessWidget, FramelessMainWindow
from PyQt5.QtWidgets import QApplication, QTextEdit


class Window(FramelessMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Winter Is Coming')
        self.setWindowIcon('./Stark-icon.png')

        titleBar = self.getTitleBar()
        titleBar.setTitleBarFont(QFont('Arial', 12))
        titleBar.setIconSize(24, 24)

        lay = self.centralWidget().layout()
        lay.addWidget(QTextEdit())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    titlebar = window.getTitleBar()
    titlebar.setTitleBarHint(['min', 'max', 'close'])
    window.show()
    sys.exit(app.exec())