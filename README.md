# pyqt-frameless-window
PyQt Frameless Window

## Feature
* Frameless
* Using Windows API (for Windows OS effect - shadow, rounded, animation, etc.) 
* Supports PyQt5, PySide2, PySide6
* User can make it enable/disable to move, resize
* Supports QWidget, QDialog, QMainWindow

## Note
I have no macOS and linux so i couldn't manage to support them as well.

Maybe i can use the virtual machine or something to do it.

There is no title bar for Windows! I will make it as soon as possible.

## Requirements
* PyQt5 - Use QtWinExtras to use Windows API feature in Qt (Qt6 doesn't support QtWinExtras anymore, sadly) 
* qtpy - To use PyQt5, PySide2(Qt version 5), PySide6(Qt version 6)

## Setup

### New version (using Windows API)

`python -m pip install pyqt-frameless-window`

### Classic version

`python -m pip install pyqt-frameless-window==0.0.61`

## Class Overview
* FramelessWidget - frameless QWidget
* FramelessDialog - frameless QDialog
* FramelessMainWindow - frameless QMainWindow

## Method Overview
### for Windows & The Others
* `setResizable(f: bool)` - Set resizable/none-resizable
* `isResizable() -> bool` - Check if window is resizable or not
* `setPressToMove(f: bool)` - Set movable/non-movable
* `isPressToMove() -> bool` - Check if window is movable or not
### The Others
* `setMargin(margin: int)` - Set the margin which allows cursor to change its shape to resize form
* `setFrameColor(color)` - Set the background color. color argument type can be both QColor and str.
* `getFrameColor` -> QColor - Get the background color.
* `setVerticalExpandedEnabled(f: bool)` - Make it able to expand vertically when double-clicking the top or bottom edges of the window.

## Example
### PyQt5 Code Sample
```python
import sys

from pyqt_frameless_window import FramelessDialog
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QTextBrowser


class Window(FramelessDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Basic Window Example')

        self.__minBtn = QPushButton('Min')
        self.__maxBtn = QPushButton('Max')
        self.__maxBtn.setCheckable(True)
        self.__fullScreenBtn = QPushButton('FullScreen')
        self.__fullScreenBtn.setCheckable(True)
        self.__closeBtn = QPushButton('Close')

        self.__minBtn.clicked.connect(self.showMinimized)
        self.__maxBtn.toggled.connect(self.__maximize)
        self.__fullScreenBtn.toggled.connect(self.__fullScreen)
        self.__closeBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.addWidget(self.__fullScreenBtn)
        lay.addWidget(self.__minBtn)
        lay.addWidget(self.__maxBtn)
        lay.addWidget(self.__closeBtn)
        lay.setSpacing(0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(QTextBrowser())

        self.setLayout(lay)

    def __maximize(self, f):
        if f:
            self.showMaximized()
        else:
            self.showNormal()

    def __fullScreen(self, f):
        if f:
            self.showFullScreen()
        else:
            self.showNormal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
```

### PySide6 Code Sample
```python
import sys

# IMPORTANT!!!!!!!!!
# to prevent the "QWidget: Must construct a QApplication before a QWidget" error, you should put the code below
from PySide6.QtCore import Qt

from pyqt_frameless_window import FramelessDialog
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QTextBrowser


class Window(FramelessDialog):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Basic Window Example')

        self.__minBtn = QPushButton('Min')
        self.__maxBtn = QPushButton('Max')
        self.__maxBtn.setCheckable(True)
        self.__fullScreenBtn = QPushButton('FullScreen')
        self.__fullScreenBtn.setCheckable(True)
        self.__closeBtn = QPushButton('Close')

        self.__minBtn.clicked.connect(self.showMinimized)
        self.__maxBtn.toggled.connect(self.__maximize)
        self.__fullScreenBtn.toggled.connect(self.__fullScreen)
        self.__closeBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.addWidget(self.__fullScreenBtn)
        lay.addWidget(self.__minBtn)
        lay.addWidget(self.__maxBtn)
        lay.addWidget(self.__closeBtn)
        lay.setSpacing(0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(QTextBrowser())

        self.setLayout(lay)

    def __maximize(self, f):
        if f:
            self.showMaximized()
        else:
            self.showNormal()

    def __fullScreen(self, f):
        if f:
            self.showFullScreen()
        else:
            self.showNormal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
``` 

### Result

![image](https://user-images.githubusercontent.com/55078043/198822265-c427574a-6595-43a1-9a2c-30359368f1b2.png)

Try to move and resize it.

Note: I tested in Windows 11, PySide6.

## See Also

<a href="https://github.com/yjg30737/pyqt-frameless-window/tree/b84dd1ba421aa7f3f940229ce6379611380f5e35">Classic version README</a> - not using Windows API, qtpy, just good old PyQt5. Enable to resize and move as always. (clunky in Windows though) 
