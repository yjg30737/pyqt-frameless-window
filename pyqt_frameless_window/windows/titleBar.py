from qtpy.QtGui import QFont
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout


class TitleBar(QWidget):
    def __init__(self, base_widget=None, hint: list = ['full_screen', 'min', 'max', 'close']):
        super().__init__(base_widget)
        self.__initVal(hint)
        self.__initUi()

    def __initVal(self, hint):
        self.__fullScreenBtn = QPushButton('▣')
        self.__minBtn = QPushButton('🗕')
        self.__maxBtn = QPushButton('🗖')
        self.__closeBtn = QPushButton('🗙')

        self.__maxBtn.setCheckable(True)
        self.__fullScreenBtn.setCheckable(True)

        self.__btn_dict = {
            'full_screen': self.__fullScreenBtn,
            'min': self.__minBtn,
            'max': self.__maxBtn,
            'close': self.__closeBtn
        }

        self.__fullScreenBtn.clicked.connect(self.__fullScreen)
        self.__minBtn.clicked.connect(self.window().showMinimized)
        self.__maxBtn.clicked.connect(self.__maximize)
        self.__closeBtn.clicked.connect(self.window().close)

        self.__hint = hint

    def __initUi(self):
        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.setAlignment(Qt.AlignRight)

        for k in self.__hint:
            if k in self.__btn_dict:
                lay.addWidget(self.__btn_dict[k])

        self.setLayout(lay)

        self._styleInit()

        # raise - helps the button widget not to be blocked by something else
        self.raise_()

        self.window().installEventFilter(self)

    def _styleInit(self):
        for btn in self.__btn_dict.values():
            btn.setStyleSheet('QPushButton { '
                              'background-color: transparent; '
                              'border: 0;'
                              'width: 50;'
                              'height: 32;'
                              '}'
                              'QPushButton:hover {'
                              'background-color: #ddd;'
                              '}'
                              'QPushButton:pressed {'
                              'background-color: #aaa;'
                              '}'
                              'QPushButton:checked {'
                              'background-color: #ddd;'
                              '}')

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
                if self.window().isMaximized():
                    self.__maxBtn.setText('🗗')
                else:
                    self.__maxBtn.setText('🗖')

        return super().eventFilter(obj, e)