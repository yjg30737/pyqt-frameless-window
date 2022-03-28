from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QColor
from PyQt5.QtWidgets import QWidget


class FramelessWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._resizing = False
        self._resizable = True

        self._margin = 3
        self._cursor = QCursor()
        self._pressToMove = False

        self.__initPosition()
        self.__initBasicUi()

    def __initBasicUi(self):
        self.setMinimumSize(self.sizeHint().width(), self.sizeHint().height())
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)

    # init the edge direction for set correct reshape cursor based on it
    def __initPosition(self):
        self.__top = False
        self.__bottom = False
        self.__left = False
        self.__right = False

    def __setCursorShapeForCurrentPoint(self, p):
        # give the margin to reshape cursor shape
        rect = self.rect()
        rect.setX(self.rect().x() + self._margin)
        rect.setY(self.rect().y() + self._margin)
        rect.setWidth(self.rect().width() - self._margin * 2)
        rect.setHeight(self.rect().height() - self._margin * 2)

        self._resizing = rect.contains(p)
        if self._resizing:
            # resize end
            self.unsetCursor()
            self._cursor = self.cursor()
            self.__initPosition()
        else:
            # resize start
            x = p.x()
            y = p.y()

            x1 = self.rect().x()
            y1 = self.rect().y()
            x2 = self.rect().width()
            y2 = self.rect().height()

            self.__left = abs(x - x1) <= self._margin # if mouse cursor is at the almost far left
            self.__top = abs(y - y1) <= self._margin # far top
            self.__right = abs(x - (x2 + x1)) <= self._margin # far right
            self.__bottom = abs(y - (y2 + y1)) <= self._margin # far bottom

            # set the cursor shape based on flag above
            if self.__top and self.__left:
                self._cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__top and self.__right:
                self._cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__left:
                self._cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__right:
                self._cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__left:
                self._cursor.setShape(Qt.SizeHorCursor)
            elif self.__top:
                self._cursor.setShape(Qt.SizeVerCursor)
            elif self.__right:
                self._cursor.setShape(Qt.SizeHorCursor)
            elif self.__bottom:
                self._cursor.setShape(Qt.SizeVerCursor)
            self.setCursor(self._cursor)

        self._resizing = not self._resizing

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self._resizing:
                self._resize()
            else:
                if self._pressToMove:
                    self._move()
        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self.isResizable():
            self.__setCursorShapeForCurrentPoint(e.pos())
        return super().mouseMoveEvent(e)

    # prevent accumulated cursor shape bug
    def enterEvent(self, e):
        if self.isResizable():
            self.__setCursorShapeForCurrentPoint(e.pos())
        return super().enterEvent(e)

    def _resize(self):
        window = self.window().windowHandle()
        # reshape cursor for resize
        if self._cursor.shape() == Qt.SizeHorCursor:
            if self.__left:
                window.startSystemResize(Qt.LeftEdge)
            elif self.__right:
                window.startSystemResize(Qt.RightEdge)
        elif self._cursor.shape() == Qt.SizeVerCursor:
            if self.__top:
                window.startSystemResize(Qt.TopEdge)
            elif self.__bottom:
                window.startSystemResize(Qt.BottomEdge)
        elif self._cursor.shape() == Qt.SizeBDiagCursor:
            if self.__top and self.__right:
                window.startSystemResize(Qt.TopEdge | Qt.RightEdge)
            elif self.__bottom and self.__left:
                window.startSystemResize(Qt.BottomEdge | Qt.LeftEdge)
        elif self._cursor.shape() == Qt.SizeFDiagCursor:
            if self.__top and self.__left:
                window.startSystemResize(Qt.TopEdge | Qt.LeftEdge)
            elif self.__bottom and self.__right:
                window.startSystemResize(Qt.BottomEdge | Qt.RightEdge)

    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()

    def setMargin(self, margin: int):
        self._margin = margin
        self.layout().setContentsMargins(self._margin, self._margin, self._margin, self._margin)

    def isResizable(self) -> bool:
        return self._resizable

    def setResizable(self, f: bool):
        self._resizable = f

    def isPressToMove(self) -> bool:
        return self._pressToMove

    def setPressToMove(self, f: bool):
        self._pressToMove = f

    def setFrameColor(self, color):
        if isinstance(color, str):
            color = QColor(color)
        self.setStyleSheet(f'background-color: {color.name()}')