from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QFocusEvent
from PySide6.QtCore import Qt

import config
from lower import Lower
from upper import Upper
import sys


class Todo(QWidget):
    def __init__(self, config, app):
        super(Todo, self).__init__()
        self.config = config
        self.app = app
        self.app.setPalette(self.config.get_palette()())

        # configure self
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setWindowTitle("minGUItodo")
        self.setWindowIcon(QIcon('resources/logo.png'))  # currently a joke
        self.setFocusPolicy(Qt.StrongFocus)

        # create main layout
        self.main = QVBoxLayout()
        self.upper = Upper(self.config["height"] * 0.8, self.config["width"], self)
        self.lower = Lower(self.config["height"] * 0.2, self.config["height"] * 0.8, self)
        self.main.addWidget(self.upper)
        self.main.addWidget(self.lower)

        self.setLayout(self.main)
        self.update()
        self.show()

    def focusInEvent(self, event: QFocusEvent):
        super().focusInEvent(event)
        self.lower.refresh()


if __name__ == "__main__":
    app = QApplication()
    app.setStyle('Fusion')
    config = config.Config()
    mainwindow = Todo(config, app)
    mainwindow.show()
    sys.exit(app.exec_())
