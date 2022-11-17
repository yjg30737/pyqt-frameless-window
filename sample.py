import sys

# IMPORTANT!!!!!!!!!
# to prevent the "QWidget: Must construct a QApplication before a QWidget" error, you should put the code below
from PySide6.QtCore import Qt

from pyqt_frameless_window import FramelessDialog
from PySide6.QtWidgets import QApplication, QTextEdit, QWidget


class Window(FramelessDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Winter Is Coming')
        self.setWindowIcon('./Stark-icon.png')
        self.setTitleBarVisible(True)

        emptyWidgetToMove = QWidget()
        emptyWidgetToMove.setFixedHeight(100)
        emptyWidgetToMove.setStyleSheet('QWidget { background-color: #ddd; }')

        lay = self.layout()
        lay.addWidget(emptyWidgetToMove)
        lay.addWidget(QTextEdit())
        self.setLayout(lay)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())