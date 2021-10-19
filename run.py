import sys, time
from socket import *
from struct import *
from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import (QApplication,QLabel,QMainWindow,QPushButton,QVBoxLayout,QWidget)




class Runnable(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        self.initialiseUDPCon()
        for i in range(1000):
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

            window.gearLabel.setText(str(self.gearFinal))
            # window.speedLabel.setText("hello World")

            
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

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.runTasks()

    def setupUi(self):
        self.setWindowTitle("Wheel Dash")
        self.setGeometry(0, 0, 720, 720)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.gearLabel = QLabel("N")
        self.gearLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.speedLabel = QLabel("N")
        # self.speedLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.gearLabel)
        # layout.addWidget(self.speedLabel)
        self.centralWidget.setLayout(layout)

    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()
        runnable = Runnable()
        pool.start(runnable)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())