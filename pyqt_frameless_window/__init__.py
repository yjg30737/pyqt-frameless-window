import platform

if platform.system() == 'Windows':
    from pyqt_frameless_window.framelessWindow import FramelessWidget, FramelessDialog, FramelessMainWindow