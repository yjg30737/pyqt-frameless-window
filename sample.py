import sys

# IMPORTANT!!!!!!!!!
# to prevent the "QWidget: Must construct a QApplication before a QWidget" error, you should put the code below
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from pyqt_frameless_window import FramelessDialog, FramelessWidget, FramelessMainWindow
from PySide6.QtWidgets import QApplication, QTextEdit


class Window(FramelessDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Winter Is Coming')
        self.setWindowIcon('./Stark-icon.png')

        # titleBar = self.getTitleBar()
        # titleBar.setTitleBarFont(QFont('Arial', 24))
        # titleBar.setIconSize(32, 32)

        lay = self.layout()
        lay.addWidget(QTextEdit())
        self.setLayout(lay)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    titlebar = window.getTitleBar()
    titlebar.setTitleBarHint(['full_screen', 'min', 'close'])
    window.show()
    sys.exit(app.exec())