import os

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon, QPixmap, QImage
from qtpy.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy


class TitleBar(QWidget):
    def __init__(self, base_widget=None, hint=None):
        super().__init__(base_widget)
        if hint is None:
            hint = ['min', 'max', 'close']
        self.__initVal(hint)
        self.__initUi()

    def __initVal(self, hint):
        # TODO
        # iconBtn
        self.__iconLbl = QLabel()

        icon = QIcon()
        icon.addFile(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Stark-icon.png'))
        self.__iconLbl.setPixmap(icon.pixmap(18, 18))

        # title label
        self.__titleLbl = QLabel()
        self.__titleLbl.setText('Winter Is Coming')

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

        # TODO refactoring
        self.__iconLbl.setStyleSheet('QLabel {'
                                     'margin-left: 4;'
                                     '}')

        self.__titleLbl.setStyleSheet('QLabel {'
                                     'margin-left: 4;'
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