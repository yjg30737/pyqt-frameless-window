# pyqt-frameless-window
PyQt frameless window

## Requirements
* PyQt5 >= 5.15 - to call <a href="https://doc.qt.io/qt-5/qwindow.html#startSystemMove">startSystemMove</a>, <a href="https://doc.qt.io/qt-5/qwindow.html#startSystemResize">startSystemResize</a> which are introduced in Qt 5.15.

## Setup
`python -m pip install pyqt-frameless-window`

## Detailed Description
This is the empty window which has no frame. It looks nothing special, but it has a great feature.

<b>It can be movable and resizable.</b> That's not the only feature. 

When you place the mouse cursor over the edge of the window, mouse cursor's shape will turn into one of those below based on direction of edge.

<a href="https://doc.qt.io/qt-5/qt.html#CursorShape-enum">CursorShape in Qt Documentations</a>
* Qt.SizeVerCursor
* Qt.SizeHorCursor
* Qt.SizeBDiagCursor
* Qt.SizeFDiagCursor

The window's minimum size is set to inner widget's recommended minimum size.

You can use this as a parent class if you want to make movable, resizable frameless window. This is no use on its own.

If you want to customize the title bar easily than use <a href="https://github.com/yjg30737/pyqt-custom-titlebar-setter">pyqt-custom-titlebar-setter</a>, which also uses the pyqt-frameless-window.

If you don't need any title bar or min/max/close buttons or something like that, just use this as a parent class of your widget.

It can expand vertically when double-clicking the top or bottom edges of the window. Minor bug still remains, but it is not fatal at all. 

## Method Overview
* `setResizable(f: bool)` - Set resizable/none-resizable
* `isResizable() -> bool` - Check if window is resizable or not
* `setPressToMove(f: bool)` - Set movable/non-movable
* `isPressToMove() -> bool` - Check if window is movable or not
* `setMargin(margin: int)` - Set the margin which allows cursor to change its shape to resize form
* `setFrameColor(color)` - Set the background color. `color` argument type can be both `QColor` and `str`.
* `getFrameColor -> QColor` - Get the background color.
* `setVerticalExpandedEnabled(f: bool)` - Make it able to expand vertically when double-clicking the top or bottom edges of the window.

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

Try to move and resize it.

## See Also
* <a href="https://github.com/yjg30737/pyqt-shadow-frame-window-example">pyqt-shadow-frame-window-example</a> - Frameless window feature + rounded corner and shadow effect.

