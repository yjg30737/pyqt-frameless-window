from ctypes import cast
from winreg import ConnectRegistry, HKEY_CURRENT_USER, OpenKey, KEY_READ, QueryValueEx

import win32con
import win32gui

from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QCursor, QIcon, QPalette, QColor, QGuiApplication
from qtpy.QtWidgets import QWidget

from ctypes.wintypes import LPRECT, MSG

from pyqt_frameless_window.windows.src import win32utils
from pyqt_frameless_window.windows.src.c import LPNCCALCSIZE_PARAMS
from pyqt_frameless_window.windows.src.windowEffect import WindowsEffectHelper
from pyqt_frameless_window.windows.titleBar import TitleBar


class BaseWidget(QWidget):
    changedToDark = Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _initVal(self):
        self._pressToMove = True
        self._resizable = True
        self._border_width = 5

        self.__detect_theme_flag = True

    def _initUi(self, hint=None):
        if hint is None:
            hint = ['min', 'max', 'close']
        self._windowEffect = WindowsEffectHelper()

        # remove window border
        # seems kinda pointless(though if you get rid of code below frame will still be seen), but if you don't add this, cursor won't properly work
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # add DWM shadow and window animation
        self._windowEffect.setBasicEffect(self.winId(), hint)

        self.windowHandle().screenChanged.connect(self._onScreenChanged)

        self._titleBar = TitleBar(self, hint)

        self.__setCurrentWindowsTheme()

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
        self._titleBar.setPressToMove(f)

    # set Windows theme by referring registry key
    def __setCurrentWindowsTheme(self):
        try:
            root = ConnectRegistry(None, HKEY_CURRENT_USER)
            root_key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', 0, KEY_READ)
            lightThemeValue, regtype = QueryValueEx(root_key, 'AppsUseLightTheme')
            if lightThemeValue == 0 or lightThemeValue == 1:
                dark_f = lightThemeValue == 0
                if dark_f:
                    pass
                    # QGuiApplication.setPalette(QPalette(QColor(0, 0, 0)))
                else:
                    pass
                    # QGuiApplication.setPalette(QPalette(QColor(255, 255, 255)))
                self._windowEffect.setDarkTheme(self.winId(), dark_f)
                self.changedToDark.emit(dark_f)
            else:
                raise Exception(f'Unknown value "{lightThemeValue}".')
        except FileNotFoundError:
            print('AppsUseLightTheme not found.')
        except Exception as e:
            print(e)

    def setDarkTheme(self, f: bool):
        self._windowEffect.setDarkTheme(self.winId(), f)

    def isDetectingThemeAllowed(self):
        return self.__detect_theme_flag

    def allowDetectingTheme(self, f: bool):
        self.__detect_theme_flag = f

    def isResizable(self) -> bool:
        return self._resizable

    def setResizable(self, f: bool):
        self._resizable = f
        self._titleBar.setBaseWindowResizable(f)

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

                    # to support snap layouts
                    # more info - https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/apply-snap-layout-menu
                    # if win32gui.PtInRect((10, 10, 100, 100), (x, y)):
                    #     return True, win32con.HTMAXBUTTON

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
            elif msg.message == win32con.WM_SETTINGCHANGE:
                if self.__detect_theme_flag:
                    self.__setCurrentWindowsTheme()
        return super().nativeEvent(e, message)

    def _onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    def setWindowIcon(self, filename):
        icon = QIcon()
        icon.addFile(filename)
        self._titleBar.setIcon(icon)
        super().setWindowIcon(icon)

    def setWindowTitle(self, title: str) -> None:
        super().setWindowTitle(title)
        self._titleBar.setTitle(title)

    def setTitleBarVisible(self, f):
        self._titleBar.setVisible(f)
        if self.isPressToMove() or self._titleBar.isPressToMove():
            self._titleBar.setPressToMove(f)
            self.setPressToMove(not f)

    def setTitleBarHint(self, hint: list):
        self._titleBar.setTitleBarHint(hint)

    def getTitleBar(self):
        return self._titleBar

    def setFixedSize(self, width, height):
        super().setFixedSize(width, height)
        self.setResizable(False)