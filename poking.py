from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 720, 720)
        self.setWindowTitle("PyQt5 window")
        self.show()
    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black,  5, Qt.DotLine))
        self.painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        self.painter.drawRect(350,350, 40, 40)


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())




