from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy


class TitleBar(QWidget):
    def __init__(self, base_widget=None, hint=None):
        super().__init__(base_widget)
        self.__initVal(hint)
        self.__initUi()

    def __initVal(self, hint):
        self._pressToMove = True
        # for make this to recognize that the base window is able to resize or not
        # this is indeed really weird way to program so i'll figure out other way to handle it soon enough
        self.__baseWindowResizable = True

        # iconLabel
        self.__iconLbl = QLabel()

        # title label
        self.__titleLbl = QLabel()

        # buttons
        self.__fullScreenBtn = QPushButton('▣')
        self.__minBtn = QPushButton('🗕')
        self.__maxBtn = QPushButton('🗖')
        self.__closeBtn = QPushButton('🗙')

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

        lay.addWidget(self.__iconLbl)
        lay.addWidget(self.__titleLbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))

        for k in self.__hint:
            if k in self.__btn_dict:
                lay.addWidget(self.__btn_dict[k])

        self._styleInit()

        self.window().installEventFilter(self)

        self.setLayout(lay)

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

        label_style = 'QLabel { margin: 4 }'

        # TODO refactoring
        self.__iconLbl.setStyleSheet(label_style)
        self.__titleLbl.setStyleSheet(label_style)

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
        if self.__baseWindowResizable:
            if event.button() != Qt.LeftButton:
                return
            self.__maximize()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self._pressToMove:
                self._move()
        return super().mousePressEvent(e)

    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == 105:
                self.__fullScreenBtn.setChecked(self.window().isFullScreen())
                self.__maxBtn.setChecked(self.window().isMaximized())
                if self.window().isMaximized():
                    self.__maxBtn.setText('🗗')
                else:
                    self.__maxBtn.setText('🗖')
                if self.window().isFullScreen():
                    self.hide()
                else:
                    self.show()

        return super().eventFilter(obj, e)

    def setIcon(self, icon):
        self.__iconLbl.setPixmap(icon.pixmap(18, 18))

    def setTitle(self, title):
        self.__titleLbl.setText(title)

    def setPressToMove(self, f: bool):
        self._pressToMove = f

    def isPressToMove(self) -> bool:
        return self._pressToMove

    def setTitleBarHint(self, hint: list):
        print(hint)

    def getIcon(self) -> QLabel:
        return self.__iconLbl

    def getTitle(self) -> QLabel:
        return self.__titleLbl

    # this is indeed really weird way to program so i'll figure out other way to handle it soon enough
    def setBaseWindowResizable(self, f: bool):
        self.__baseWindowResizable = f
        self.__maxBtn.setVisible(f)