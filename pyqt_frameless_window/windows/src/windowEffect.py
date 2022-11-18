from ctypes import byref, windll

import win32con
import win32gui

from .c import MARGINS


class WindowsEffectHelper:

    def __init__(self):
        # C Libraries which are really necessary to apply Windows OS effect to Qt frameless window
        user32 = windll.LoadLibrary("user32")
        dwmapi = windll.LoadLibrary("dwmapi")
        
        self.__windowCompositionAttribute = user32.SetWindowCompositionAttribute
        self.__dwmExtendFrameIntoClientArea = dwmapi.DwmExtendFrameIntoClientArea
        self.__dwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute

    # set fancy effect
    def setBasicEffect(self, hWnd):
        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.__dwmExtendFrameIntoClientArea(hWnd, byref(margins))

        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            win32con.WS_MINIMIZEBOX
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )

# TODO
# should make it unable to maximize with snapping in a dynamical way
# win32gui.SetWindowLong(
#             hWnd,
#             win32con.GWL_STYLE,
#             win32con.WS_MINIMIZEBOX
#             | win32con.WS_CAPTION
#             | win32con.CS_DBLCLKS
#             | win32con.WS_THICKFRAME,
#         )