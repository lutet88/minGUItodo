from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QRect, Slot
import command_handler


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)


class CommandField(QLineEdit):
    def __init__(self, window, tooltip):
        super(CommandField, self).__init__()
        self.win = window
        self.tooltip = tooltip
        self.returnPressed.connect(self.return_pressed)
        self.textEdited.connect(self.text_changed)
        self.commandHandler = command_handler.CommandHandler(window)

    def return_pressed(self):
        text = self.text().strip()
        command = text.split(" ")[0]
        result = self.commandHandler.handle(command, text)
        self.setPlaceholderText(result)
        self.clear()
        self.text_changed()

    def text_changed(self):
        text = self.text().strip()
        if text.split(" "):
            command = text.split(" ")[0]
            self.tooltip.setText(self.commandHandler.tooltip(command))


class Lower(QWidget):
    def __init__(self, height, offset, window):
        super(Lower, self).__init__()
        self.win = window

        self.setFixedHeight(height)
        # self.move(0, offset)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.uppertext = QLabel()
        self.lowertext = QLabel()
        self.upperline = QHLine()
        self.commandbox = CommandField(self.win, self.lowertext)

        # config self
        self.layout.addWidget(self.upperline)
        self.layout.addWidget(self.uppertext)
        self.layout.addWidget(self.commandbox)
        self.layout.addWidget(self.lowertext)

        # config upper text
        self.uppertext.setMinimumHeight(28)
        self.uppertext.setMaximumHeight(28)
        self.uppertext.setText("enter commands below")
        self.uppertext.setAlignment(Qt.AlignLeft)
        self.uppertext.setAlignment(Qt.AlignBottom)

        # config lower text
        self.lowertext.setMinimumHeight(28)
        self.lowertext.setMaximumHeight(28)
        self.lowertext.setText("")
        self.lowertext.setAlignment(Qt.AlignLeft)
        self.lowertext.setAlignment(Qt.AlignTop)

        # config line
        self.upperline.setLineWidth(3)
        self.upperline.setMidLineWidth(3)
