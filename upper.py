from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QRect, Slot
import datetime
import pytz

timezone_offset = 60 * 60 * 8


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
        print("[INFO] top line geometry:", str(self.geometry())[21:-1])


class Upper(QWidget):
    def __init__(self, height, width, window):
        super(Upper, self).__init__()
        self.win = window

        self.setFixedHeight(height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.leftbox = QVBoxLayout()
        self.leftbox.spacer = QSpacerItem(width * 0.5 - 1, height)
        self.leftbox.addSpacerItem(self.leftbox.spacer)
        self.leftWidget = QWidget()
        self.rightbox = QVBoxLayout()
        self.rightWidget = QWidget()
        self.midline = QVLine()
        self.midline.setMinimumHeight(height * 0.91)
        self.midline.setMaximumHeight(height * 0.96)
        self.days = []

        self.leftWidget.setLayout(self.leftbox)
        self.rightWidget.setLayout(self.rightbox)
        self.leftWidget.setMaximumWidth(width * 0.5 - 1)
        self.rightWidget.setMaximumWidth(width * 0.5 - 1)

        # config self
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.leftWidget)
        self.layout.addWidget(self.midline)
        self.layout.addWidget(self.rightWidget)
        self.layout.setAlignment(Qt.AlignTop)

        # config line
        self.midline.setLineWidth(3)
        self.midline.setMidLineWidth(3)

        # config boxes
        self.boxes = []
        """"# test DayBox
        dbox = DayBox("Feb 15, 2021", 100)
        self.leftbox.addWidget(dbox)
        dbox.refresh(["8:00 - do this", "9:00 - do that"])"""

    def refreshTopLeft(self, db):
        # kill existing boxes
        for box in self.boxes:
            self.leftbox.removeWidget(box)
            box.delete()
        # remove existing QSpacingItem
        self.leftbox.removeItem(self.leftbox.spacer)

        self.boxes = []

        # get query from sqlite
        today = int(datetime.datetime.now().timestamp() + timezone_offset) // 86400 * 86400
        prevtasks = db.queryTasks(0, today - 1)
        latest = db.getLatestTimestamp()
        tasks = db.queryTasks(today, latest if latest > today else today)

        # todate = today / 86400
        # split into days
        days = {}
        # print(tasks)
        for task in tasks:
            day = (task[1] + timezone_offset) // 86400
            # print(day, task)
            if not day in days:
                days[day] = [task]
            else:
                days[day].append(task)
        # process by day (into each DayBox)
        for day in days:
            tasks = []
            for taskdata in days[day]:
                time = datetime.datetime.fromtimestamp(taskdata[1]).strftime("%H:%M")
                name = taskdata[2]
                due = "" if taskdata[4] == 0 else \
                    "(Due " + datetime.datetime.fromtimestamp(taskdata[4]).strftime("%b %d @ %H:%M") + ")"
                hexid = hex(taskdata[0])[2:]
                s = "[" + hexid + "] " + time + " - " + name + " " + due
                tasks.append((s, taskdata[5], taskdata[1]))
            dbox = DayBox(datetime.datetime.fromtimestamp(day * 86400 + 1).strftime("%B") +
                          " " + str(int(datetime.datetime.fromtimestamp(day * 86400 + 1).strftime("%d"))), day)
            tasks.sort(key=lambda x: x[2])
            dbox.refresh(tasks)
            self.boxes.append(dbox)
            self.leftbox.addWidget(dbox)
        # print(self.boxes)
        self.leftbox.addSpacerItem(self.leftbox.spacer)
        self.win.update()


class DayBox(QWidget):
    def __init__(self, day, dayval):
        super(DayBox, self).__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.daylabel = QLabel()
        self.layout.addWidget(self.daylabel)
        self.daylabel.setText(day)
        self.dayValue = dayval
        self.tasks = []
        self.tasklabels = []
        policy = QSizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Minimum)
        policy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)
        self.setSizePolicy(policy)

    def refresh(self, tasks):
        self.tasks = tasks
        for tasklabel in self.tasklabels:
            self.layout.removeWidget(tasklabel)
            del tasklabel
        self.tasklabels = []
        for task in self.tasks:
            tl = QLabel()
            tl.setText(task[0])
            # stylize
            if task[1]:
                # completed
                tl.setStyleSheet("QLabel { color : #96fa9d; }")
            else:
                # not complete
                if task[2] < datetime.datetime.now().timestamp():
                    # late
                    tl.setStyleSheet("QLabel { color: #fa969d; }")
                else:
                    # everything else
                    tl.setStyleSheet("QLabel { color : white; }")
            self.layout.addWidget(tl)

    def delete(self):
        try:
            self.daylabel.setText("")
            self.hide()
            for tasklabel in self.tasklabels:
                tasklabel.setText("")
                tasklabel.deleteLater()
                self.layout.removeWidget(tasklabel)
            self.setLayout(None)
            self.deleteLater()
        except RuntimeError:
            del self
