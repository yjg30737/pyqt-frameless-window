# pyqt-frameless-window
PyQt frameless window

## Requirements
* PyQt5 >= 5.15 - to call <a href="https://doc.qt.io/qt-5/qwindow.html#startSystemMove">startSystemMove</a>, <a href="https://doc.qt.io/qt-5/qwindow.html#startSystemResize">startSystemResize</a> which are introduced in Qt 5.15.

## Setup
`python -m pip install pyqt-frameless-window`

## Usage
This is the empty window which has no frame. It looks nothing special, but it has a great feature.

<b>It can be movable and resizable.</b> That's not the only feature. 

When you place the mouse cursor over the edge of the window, mouse cursor's shape will turn into one of those below based on direction of edge.

* Qt.SizeVerCursor
* Qt.SizeHorCursor
* Qt.SizeBDiagCursor
* Qt.SizeFDiagCursor

The window's minimum size is set to inner widget's recommended minimum size.

You can use this as a super class if you want to make movable, resizable, cursor-reshapable frameless window. This is no use on its own.

<a href="https://github.com/yjg30737/pyqt-custom-titlebar-window.git">pyqt-custom-titlebar-window</a>(pacakge which helps to make custom titlebar) is using pyqt-frameless-window.

## Method Overview
* ```setResizable(f: bool)``` - Set resizable/none-resizable
* ```isResizable() -> bool``` - Check the window is resizable or not
* ```setPressToMove(f: bool)``` - Set movable/none-movable dragging the window
* ```setMargin(margin: int)``` - Set the margin which allows cursor to change its shape to resize form.

## Example
Code Sample
```python
from PyQt5.QtWidgets import QApplication
from pyqt_frameless_window import FramelessWindow


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = FramelessWindow()
    ex.show()
    sys.exit(app.exec_())
```

Result

![image](https://user-images.githubusercontent.com/55078043/151485588-eea83a1b-7150-4a37-b0f1-6891d5f3da1f.png)
