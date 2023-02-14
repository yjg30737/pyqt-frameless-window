import platform

if platform.system() == 'Windows':
    from pyqt_frameless_window.windows.baseWidget import BaseWidget
else:
    from pyqt_frameless_window.base.baseWidget import BaseWidget

from qtpy.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QWidget
from qtpy.QtCore import Signal



class FramelessWidget(BaseWidget):
    changedToDark = Signal(bool)

    def __init__(self, hint=None):
        super().__init__()
        self._initVal()
        self._initUi(hint)

    def _initUi(self, hint):
        super()._initUi(hint)
        lay = QVBoxLayout()
        lay.addWidget(self._titleBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.setLayout(lay)


class FramelessDialog(QDialog, BaseWidget):
    changedToDark = Signal(bool)
    def __init__(self, hint=None):
        super().__init__()
        self._initVal()
        self._initUi(hint)

    def _initUi(self, hint):
        super()._initUi(hint)
        lay = QVBoxLayout()
        lay.addWidget(self._titleBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.setLayout(lay)


class FramelessMainWindow(QMainWindow, BaseWidget):
    changedToDark = Signal(bool)
    def __init__(self, hint=None):
        super().__init__()
        self._initVal()
        self._initUi(hint)

    def _initUi(self, hint):
        super()._initUi(hint)
        lay = QVBoxLayout()
        lay.addWidget(self._titleBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        mainWidget = BaseWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)
