import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QTextEdit

from pyqt_frameless_window import FramelessWidget


class Window(FramelessWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Winter Is Coming')
        self.setWindowIcon('./Stark-icon.png')

        titleBar = self.getTitleBar()
        titleBar.setTitleBarFont(QFont('Arial', 12))
        titleBar.setIconSize(24, 24)

        lay = self.layout()
        lay.addWidget(QTextEdit())
        self.setLayout(lay)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    titlebar = window.getTitleBar()
    titlebar.setTitleBarHint(['min', 'max', 'close'])
    window.show()
    sys.exit(app.exec())