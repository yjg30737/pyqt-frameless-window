import sys

# IMPORTANT!!!!!!!!!
# to prevent the "QWidget: Must construct a QApplication before a QWidget" error, you should put the code below
from PySide6.QtCore import Qt

from pyqt_frameless_window import FramelessDialog
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QTextBrowser


class Window(FramelessDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Basic Window Example')

        self.__minBtn = QPushButton('Min')
        self.__maxBtn = QPushButton('Max')
        self.__maxBtn.setCheckable(True)
        self.__fullScreenBtn = QPushButton('FullScreen')
        self.__fullScreenBtn.setCheckable(True)
        self.__closeBtn = QPushButton('Close')

        self.__minBtn.clicked.connect(self.showMinimized)
        self.__maxBtn.toggled.connect(self.__maximize)
        self.__fullScreenBtn.toggled.connect(self.__fullScreen)
        self.__closeBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.addWidget(self.__fullScreenBtn)
        lay.addWidget(self.__minBtn)
        lay.addWidget(self.__maxBtn)
        lay.addWidget(self.__closeBtn)
        lay.setSpacing(0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(QTextBrowser())

        self.setLayout(lay)

    def __maximize(self, f):
        if f:
            self.showMaximized()
        else:
            self.showNormal()

    def __fullScreen(self, f):
        if f:
            self.showFullScreen()
        else:
            self.showNormal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())