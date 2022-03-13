# pyqt-frameless-window
PyQt Frameless Window (super class is QWidget) to inherit a variety of frameless widget

## Requirements
* PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-frameless-window.git --upgrade```

## Usage
This is the empty window which has no frame. It looks nothing special, but it has a great feature.

<b>It can be movable and resizable.</b> That's not the only feature. 

When you place the mouse cursor over the edge of the window, mouse cursor's shape will turn into one of those below based on direction of edge.

* Qt.SizeVerCursor
* Qt.SizeHorCursor
* Qt.SizeBDiagCursor
* Qt.SizeFDiagCursor

The window's minimum size is set to <b>60, 60</b>.

You can use this as a super class if you want to make movable, resizable, cursor-reshapable frameless window. This is no use on its own.

## Method Overview
* ```setMargin(margin: int)``` - Set the margin which allows cursor to change its shape to resize form.
* ```setResizable(f: bool)``` - Set resizable/none resizable

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
