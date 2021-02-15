from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QRect, Slot
import datetime

class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
        print("i am line ï", self.geometry())


class Upper(QWidget):
    def __init__(self, height, width, window):
        super(Upper, self).__init__()
        self.win = window

        self.setFixedHeight(height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.leftbox = QVBoxLayout()
        self.leftWidget = QWidget()
        self.rightbox = QVBoxLayout()
        self.rightWidget = QWidget()
        self.midline = QVLine()
        self.midline.setMinimumHeight(height*0.96)
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

    def refresh(self, db):
        # kill existing boxes
        for box in self.boxes:
            self.leftbox.removeWidget(box)
            box.__del__()

        self.boxes = []

        # get query from sqlite
        today = int(datetime.datetime.now().timestamp()) // 86400 * 86400
        prevtasks = db.queryTasks(0, today-1)
        latest = db.getLatestTimestamp()
        tasks = db.queryTasks(today, latest if latest > today else today)

        todate = today / 86400
        # split into days
        days = {}
        print(tasks)
        for task in tasks:
            day = task[0] // 86400
            print(day, task)
            if not day in days:
                days[day] = [task]
            else:
                days[day].append(task)

        for day in days:
            tasks = []
            for taskdata in days[day]:
                time = datetime.datetime.fromtimestamp(taskdata[0]).strftime("%H:%M")
                name = taskdata[1]
                due = "" if taskdata[3] == 0 else "(Due "+datetime.datetime.fromtimestamp(taskdata[3]).strftime("%b %d @ %H:%M")+")"
                s = time+" - "+name+" "+due
                tasks.append(s)
            dbox = DayBox(datetime.datetime.fromtimestamp(day * 86400 + 1).strftime("%b %d"), day)
            dbox.refresh(tasks)
            self.boxes.append(dbox)
            self.leftbox.addWidget(dbox)
        print(self.boxes)
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
            tl.setText(task)
            self.layout.addWidget(tl)

    def __del__(self):
        self.daylabel.setText("")
        self.hide()
        for tasklabel in self.tasklabels:
            tasklabel.setText("")
            tasklabel.deleteLater()
            self.layout.removeWidget(tasklabel)
            #del tasklabel
        self.setLayout(None)
        self.deleteLater()
        #del self.layout
        #del self
