from ctypes import cast

import win32con
import win32gui

from qtpy.QtCore import Qt
from qtpy.QtGui import QCursor
from qtpy.QtWidgets import QWidget, QMainWindow, QDialog

from ctypes.wintypes import LPRECT, MSG

from pyqt_frameless_window.src import win32utils
from pyqt_frameless_window.src.c import LPNCCALCSIZE_PARAMS
from pyqt_frameless_window.src.windowEffect import WindowsEffectHelper


class BaseWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initVal()
        self._initUi()

    def _initVal(self):
        self._pressToMove = True
        self._resizable = True
        self._border_width = 5

    def _initUi(self):
        self._windowEffect = WindowsEffectHelper()

        # remove window border
        # seems kinda pointless(though if you get rid of code below frame will still be seen), but if you don't add this, cursor won't properly work
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # add DWM shadow and window animation
        self._windowEffect.setBasicEffect(self.winId())

        self.windowHandle().screenChanged.connect(self._onScreenChanged)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self._pressToMove:
                self._move()
        return super().mousePressEvent(e)

    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()

    def isPressToMove(self) -> bool:
        return self._pressToMove

    def setPressToMove(self, f: bool):
        self._pressToMove = f

    def isResizable(self) -> bool:
        return self._resizable

    def setResizable(self, f: bool):
        self._resizable = f

    def nativeEvent(self, e, message):
        msg = MSG.from_address(message.__int__())
        # check if it is message from Windows OS
        if msg.hWnd:
            # update cursor shape to resize/resize feature
            # get WM_NCHITTEST message
            # more info - https://learn.microsoft.com/ko-kr/windows/win32/inputdev/wm-nchittest
            if msg.message == win32con.WM_NCHITTEST:
                if self._resizable:
                    pos = QCursor.pos()
                    x = pos.x() - self.x()
                    y = pos.y() - self.y()

                    w, h = self.width(), self.height()

                    left = x < self._border_width
                    top = y < self._border_width
                    right = x > w - self._border_width
                    bottom = y > h - self._border_width

                    if top and left:
                        return True, win32con.HTTOPLEFT
                    elif top and right:
                        return True, win32con.HTTOPRIGHT
                    elif bottom and left:
                        return True, win32con.HTBOTTOMLEFT
                    elif bottom and right:
                        return True, win32con.HTBOTTOMRIGHT
                    elif left:
                        return True, win32con.HTLEFT
                    elif top:
                        return True, win32con.HTTOP
                    elif right:
                        return True, win32con.HTRIGHT
                    elif bottom:
                        return True, win32con.HTBOTTOM

            # maximize/minimize/full screen feature
            # get WM_NCCALCSIZE message
            # more info - https://learn.microsoft.com/ko-kr/windows/win32/winmsg/wm-nccalcsize
            elif msg.message == win32con.WM_NCCALCSIZE:
                if msg.wParam:
                    rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
                else:
                    rect = cast(msg.lParam, LPRECT).contents

                max_f = win32utils.isMaximized(msg.hWnd)
                full_f = win32utils.isFullScreen(msg.hWnd)

                # adjust the size of window
                if max_f and not full_f:
                    thickness = win32utils.getResizeBorderThickness(msg.hWnd)
                    rect.top += thickness
                    rect.left += thickness
                    rect.right -= thickness
                    rect.bottom -= thickness

                # for auto-hide taskbar
                if (max_f or full_f) and win32utils.Taskbar.isAutoHide():
                    position = win32utils.Taskbar.getPosition(msg.hWnd)
                    if position == win32utils.Taskbar.LEFT:
                        rect.top += win32utils.Taskbar.AUTO_HIDE_THICKNESS
                    elif position == win32utils.Taskbar.BOTTOM:
                        rect.bottom -= win32utils.Taskbar.AUTO_HIDE_THICKNESS
                    elif position == win32utils.Taskbar.LEFT:
                        rect.left += win32utils.Taskbar.AUTO_HIDE_THICKNESS
                    elif position == win32utils.Taskbar.RIGHT:
                        rect.right -= win32utils.Taskbar.AUTO_HIDE_THICKNESS

                result = 0 if not msg.wParam else win32con.WVR_REDRAW
                return True, result
        return super().nativeEvent(e, message)

    def _onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)


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


