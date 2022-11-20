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
    def setBasicEffect(self, hWnd, hint):
        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.__dwmExtendFrameIntoClientArea(hWnd, byref(margins))
        # common window value (including minimize, maximize, close, resize, animation..)
        dwNewLong = win32con.WS_CAPTION
        # if there is only close button
        if 'close' in hint and len(hint) == 1:
            pass
        else:
            # if there is min button
            if 'min' in hint:
                dwNewLong |= win32con.WS_MINIMIZEBOX
            # if there is max button (it indicates that window is resizable, so add the maximize-related values
            if 'max' in hint:
                dwNewLong |= win32con.CS_DBLCLKS | win32con.WS_THICKFRAME | win32con.WS_MAXIMIZEBOX
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            dwNewLong
        )