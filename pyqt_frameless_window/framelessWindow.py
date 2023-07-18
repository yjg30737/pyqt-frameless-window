import platform

if platform.system() == 'Windows':
    from pyqt_frameless_window.windows.baseWidget import BaseWidget, BaseDialog, BaseMainWindow
else:
    from pyqt_frameless_window.base.baseWidget import BaseWidget

from qtpy.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QWidget
from qtpy.QtCore import Signal



class FramelessWidget(BaseWidget):
    changedToDark = Signal(bool)

    def __init__(self, hint=None, flags: list = []):
        super().__init__()
        self._initVal()
        self._initUi(hint, flags)

    def _initUi(self, hint, flags):
        super()._initUi(hint, flags)
        lay = QVBoxLayout()
        lay.addWidget(self._titleBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.setLayout(lay)


class FramelessDialog(BaseDialog):
    changedToDark = Signal(bool)
    def __init__(self, hint=None, flags: list = []):
        super().__init__()
        self._initVal()
        self._initUi(hint, flags)

    def _initUi(self, hint, flags):
        super()._initUi(hint, flags)
        lay = QVBoxLayout()
        lay.addWidget(self._titleBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.setLayout(lay)


class FramelessMainWindow(BaseMainWindow):
    changedToDark = Signal(bool)

    def __init__(self, hint=None, flags: list = []):
        super().__init__()
        self._initVal()
        self._initUi(hint, flags)

    def _initUi(self, hint, flags):
        super()._initUi(hint, flags)
        lay = QVBoxLayout()
        lay.addWidget(self._titleBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)
