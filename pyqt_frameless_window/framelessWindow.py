import platform

if platform.system() == 'Windows':
    from pyqt_frameless_window.windows.baseWidget import BaseWidget
else:
    from pyqt_frameless_window.base.baseWidget import BaseWidget

from qtpy.QtWidgets import QDialog, QMainWindow


class FramelessWidget(BaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initVal()
        self._initUi()


class FramelessDialog(QDialog, BaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initVal()
        self._initUi()


class FramelessMainWindow(QMainWindow, BaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initVal()
        self._initUi()