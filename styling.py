from PySide6.QtCore import Slot,Qt
from PySide6.QtGui import QPalette, QColor


class Palette:
    def __init__(self, colormap):
        self.__palette__ = QPalette()
        for (component, color) in colormap:
            self.__palette__.setColor(component, color)

    def __call__(self):
        return self.__palette__
