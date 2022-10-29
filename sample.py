import sys

# to prevent the "QWidget: Must construct a QApplication before a QWidget" error
from PySide6.QtCore import Qt

from pyqt_frameless_window import FramelessDialog
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTabWidget, \
    QTextBrowser


class Window(FramelessDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Settings')

        self.__widget = QTextBrowser()

        topWidget = QTabWidget()
        topWidget.addTab(self.__widget, 'Timer')

        self.__okBtn = QPushButton()
        self.__okBtn.clicked.connect(self.showNormal)
        self.__okBtn.setText('OK')

        closeBtn = QPushButton()
        closeBtn.clicked.connect(self.showMaximized)
        closeBtn.setText('Cancel')

        lay = QHBoxLayout()
        lay.addWidget(self.__okBtn)
        lay.addWidget(closeBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(bottomWidget)

        self.setLayout(lay)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        return super().keyPressEvent(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())