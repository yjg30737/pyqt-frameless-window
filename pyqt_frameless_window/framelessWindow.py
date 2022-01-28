from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget


class FramelessWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._resized = False

        self._margin = 3
        self._cursor = QCursor()

        self.__initPosition()
        self.__initBasicUi()

    def __initBasicUi(self):
        self.setMinimumSize(60, 60)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)

    def __initPosition(self):
        self.__top = False
        self.__bottom = False
        self.__left = False
        self.__right = False

    def __setCursorShapeForCurrentPoint(self, p):
        rect = self.rect()
        rect.setX(self.rect().x() + self._margin)
        rect.setY(self.rect().y() + self._margin)
        rect.setWidth(self.rect().width() - self._margin * 2)
        rect.setHeight(self.rect().height() - self._margin * 2)

        self._resized = rect.contains(p)
        if self._resized:

            # cursor inside of widget
            self.unsetCursor()
            self._cursor = self.cursor()
            self.__initPosition()
        else:
            # resize
            x = p.x()
            y = p.y()

            x1 = self.rect().x()
            y1 = self.rect().y()
            x2 = self.rect().width()
            y2 = self.rect().height()

            self.__left = abs(x - x1) <= self._margin
            self.__top = abs(y - y1) <= self._margin
            self.__right = abs(x - (x2 + x1)) <= self._margin
            self.__bottom = abs(y - (y2 + y1)) <= self._margin

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

        self._resized = not self._resized

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._resize()
        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        self.__setCursorShapeForCurrentPoint(e.pos())
        return super().mouseMoveEvent(e)

    def enterEvent(self, e):
        self.__setCursorShapeForCurrentPoint(e.pos())
        return super().enterEvent(e)

    def _resize(self):
        window = self.windowHandle()
        if self._resized:
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
        window = self.windowHandle()
        if self._resized:
            pass
        else:
            window.startSystemMove()