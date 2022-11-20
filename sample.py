import sys

# IMPORTANT!!!!!!!!!
# to prevent the "QWidget: Must construct a QApplication before a QWidget" error, you should put the code below
from PySide6.QtCore import Qt

from pyqt_frameless_window import FramelessDialog, FramelessWidget, FramelessMainWindow
from PySide6.QtWidgets import QApplication, QTextEdit


class Window(FramelessMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Winter Is Coming')
        self.setWindowIcon('./Stark-icon.png')

        lay = self.layout()
        lay.addWidget(QTextEdit())
        self.setLayout(lay)
        self.setResizable(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window(['min', 'close'])
    window.show()
    sys.exit(app.exec())