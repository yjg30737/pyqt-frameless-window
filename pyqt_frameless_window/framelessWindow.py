import platform

if platform.system() == 'Windows':
    from pyqt_frameless_window.windows.baseWidget import BaseWidget
else:
    from pyqt_frameless_window.base.baseWidget import BaseWidget

from qtpy.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QWidget


class FramelessWidget(BaseWidget):
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
    def __init__(self, hint=None):
        super().__init__(hint)
        self._initVal()
        self._initUi(hint)

    def _initUi(self, hint):
        super()._initUi(hint)
        lay = QVBoxLayout()
        lay.addWidget(self._titleBar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)
