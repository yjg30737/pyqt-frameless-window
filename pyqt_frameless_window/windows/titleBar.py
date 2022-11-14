
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.__minBtn = QPushButton('Min', parent=self)
        self.__maxBtn = QPushButton('Max', parent=self)
        self.__maxBtn.setCheckable(True)
        self.__fullScreenBtn = QPushButton('FullScreen', parent=self)
        self.__fullScreenBtn.setCheckable(True)
        self.__closeBtn = QPushButton('Close', parent=self)

        self.__minBtn.clicked.connect(self.window().showMinimized)
        self.__maxBtn.clicked.connect(self.__maximize)
        self.__fullScreenBtn.clicked.connect(self.__fullScreen)
        self.__closeBtn.clicked.connect(self.window().close)

        lay = QHBoxLayout()
        lay.addWidget(self.__fullScreenBtn)
        lay.addWidget(self.__minBtn)
        lay.addWidget(self.__maxBtn)
        lay.addWidget(self.__closeBtn)
        lay.setAlignment(Qt.AlignRight)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

        self.window().installEventFilter(self)

    def __maximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def __fullScreen(self):
        if self.window().isFullScreen():
            self.window().showNormal()
        else:
            self.window().showFullScreen()

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        self.__maximize()

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == 105:
                self.__fullScreenBtn.setChecked(self.window().isFullScreen())
                self.__maxBtn.setChecked(self.window().isMaximized())

        return super().eventFilter(obj, e)