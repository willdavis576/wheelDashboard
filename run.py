import sys, time
from socket import *
from struct import *
from PyQt5.QtCore import QRunnable, Qt, QThreadPool
# from PyQt5.QtWidgets import (QApplication,QLabel,QMainWindow,QPushButton,QVBoxLayout,QWidget)
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

stylesheet = """
    window {
        background-image: url("C:/Users/Will/OneDrive - Middlesex University/Inventions/fanatec wheel/wheel rev 3/wheelDashboard/dashBackground.png)"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

class Runnable(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        self.initialiseUDPCon()
        while True:
            self.pktformat='cifff??????fffiiiifffffiffffffffffffffffff'
            self.messageback, self.ipAddress =self.clientSocket.recvfrom(16384)
            self.backString = unpack(self.pktformat, self.messageback[:152])

            self.gear = self.backString[23]
            self.speed = self.backString[3]

            if (self.gear > 1):
                self.gearFinal = self.gear - 1

            if (self.gear == 1):
                self.gearFinal = "N"

            if (self.gear == 0):
                self.gearFinal = "R"

            self.speedFinal = round(self.speed)

            window.gearLabel.setText(str(self.gearFinal))
            window.speedLabel.setText(str(self.speedFinal))

            
    def initialiseUDPCon(self):
        self.serverName='192.168.0.163'
        self.serverPort = 9996
        self.clientSocket = socket(AF_INET,SOCK_DGRAM)
        self.message=pack('iii',1,1,0)

        self.clientSocket.sendto(self.message, (self.serverName, self.serverPort))

        self.messageback, self.ipAddress=self.clientSocket.recvfrom(1024)
        self.pktformat='100s100sii100s100s'
        self.n = calcsize(self.pktformat)

        self.backString = unpack(self.pktformat, self.messageback)

        self.carName = self.backString[0].decode(errors='ignore').replace('\x00', '').split('%')[0]
        self.driverName = self.backString[1].decode(errors='ignore').replace('\x00', '').split('%')[0]
        self.trackName = self.backString[4].decode(errors='ignore').replace('\x00', '').split('%')[0]
        self.trackConfig = self.backString[5].decode(errors='ignore').replace('\x00', '').split('%')[0]

        print(self.carName, self.driverName, self.trackName)

        self.message=pack('iii',1,1,1)
        self.clientSocket.sendto(self.message, (self.serverName, self.serverPort))

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        #self.runTasks()

    def fonts(self):
        self.fontName = 'Arial'

        self.gearLabel = QLabel("N")
        self.gearLabel.setFont(QFont(self.fontName, 200))
        self.gearLabel.setStyleSheet("color:rgb(255,255,255)")
        # self.gearLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.speedLabelLabel = QLabel("SPEED")
        self.speedLabelLabel.setFont(QFont(self.fontName, 75))
        self.speedLabelLabel.setStyleSheet("color:rgb(255,255,255)")
        # self.speedLabelLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.speedLabel = QLabel("0")
        self.speedLabel.setFont(QFont(self.fontName, 200))
        self.speedLabel.setStyleSheet("color:rgb(255,255,255)")
        # self.speedLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


    def setupUi(self):
        self.setWindowTitle("Wheel Dash")
        self.setGeometry(0, 0, 720, 720)
        self.setFixedSize(720,720)
        # self.setStyleSheet("background:rgb(200,200,205)")
        self.setStyleSheet("background-image: url(C:/Users/Will/OneDrive - Middlesex University/Inventions/fanatec wheel/wheel rev 3/wheelDashboard/dashBackground.png); background-repeat: no-repeat; background-position: center;")
        # self.setStyleSheet(stylesheet)
        self.fonts()
        self.createGridLayout()
     

    def createGridLayout(self):
        layout = QGridLayout()
 
        layout.addWidget(self.gearLabel, 0,1)
        layout.addWidget(self.speedLabelLabel,1,0)
        layout.addWidget(self.speedLabel,2,0)

        self.setLayout(layout)

       


    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()
        runnable = Runnable()
        pool.start(runnable)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())