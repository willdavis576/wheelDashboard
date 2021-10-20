import sys, time
from socket import *
from struct import *
from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets

from IPython import embed

#0 is windows, 1 is pi
device = 0
backgroundLocation = ""
winBackLoc = "background-image: url(C:/Users/Will/OneDrive - Middlesex University/Inventions/fanatec wheel/wheel rev 3/wheelDashboard/dashBackground.png); background-repeat: no-repeat; background-position: center;\)"
piBackLoc = "background-image: url(/home/pi/wheelDashboard/dashBackground.png)"

if device == 0:
    backgroundLocation = winBackLoc
if device == 1:
    backgroundLocation = piBackLoc

print(backgroundLocation)

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
            self.engineRPM = round(self.backString[21])

            self.engineRPMScaled = round((self.engineRPM) * (595 / 8000))
            ui.revCounter.setFixedWidth(self.engineRPMScaled)

            if (self.gear > 1):
                self.gearFinal = self.gear - 1

            if (self.gear == 1):
                self.gearFinal = "N"

            if (self.gear == 0):
                self.gearFinal = "R"

            self.speedFinal = round(self.speed)

            ui.gearLabel.setText(str(self.gearFinal))
            ui.speedLabel.setText(str(self.speedFinal))

           
            
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.setGeometry(0,0,720,720)
        MainWindow.setMinimumSize(QtCore.QSize(720, 720))
        MainWindow.setMaximumSize(QtCore.QSize(720, 720))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setToolTipDuration(7)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(-3, 0, 723, 720))
        self.graphicsView.setStyleSheet(backgroundLocation)
        self.graphicsView.setObjectName("graphicsView")
        
        self.allWidgets()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.speedLabel.setText(_translate("MainWindow", "0"))
        self.gearLabel.setText(_translate("MainWindow", "N"))
        self.fuelLabel.setText(_translate("MainWindow", "0"))
        self.brakeBLabel.setText(_translate("MainWindow", "60"))
        self.deltaLabel.setText(_translate("MainWindow", "+0:00"))
        self.LaptimeLabel.setText(_translate("MainWindow", "00:00"))
        self.TC1Label.setText(_translate("MainWindow", "1"))
        self.TC2Label.setText(_translate("MainWindow", "1"))
        self.PFuelLabel.setText(_translate("MainWindow", "10"))

    def allWidgets(self):
        self.speedLabel = QtWidgets.QLabel(self.centralwidget)
        self.speedLabel.setGeometry(QtCore.QRect(360, 312, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.speedLabel.setFont(font)
        self.speedLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.speedLabel.setStyleSheet("color:rgb(255,255,255)")
        self.speedLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.speedLabel.setMidLineWidth(-1)
        self.speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.speedLabel.setObjectName("speedLabel")
        self.gearLabel = QtWidgets.QLabel(self.centralwidget)
        self.gearLabel.setGeometry(QtCore.QRect(283, 98, 181, 191))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(140)
        font.setBold(True)
        font.setWeight(75)
        self.gearLabel.setFont(font)
        self.gearLabel.setStyleSheet("color:rgb(255,255,255)")
        self.gearLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gearLabel.setObjectName("gearLabel")
        self.fuelLabel = QtWidgets.QLabel(self.centralwidget)
        self.fuelLabel.setGeometry(QtCore.QRect(520, 312, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.fuelLabel.setFont(font)
        self.fuelLabel.setStyleSheet("color:rgb(255,255,255)")
        self.fuelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fuelLabel.setObjectName("fuelLabel")
        self.brakeBLabel = QtWidgets.QLabel(self.centralwidget)
        self.brakeBLabel.setGeometry(QtCore.QRect(576, 400, 121, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.brakeBLabel.setFont(font)
        self.brakeBLabel.setStyleSheet("color:rgb(255,255,255)")
        self.brakeBLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.brakeBLabel.setObjectName("brakeBLabel")
        self.deltaLabel = QtWidgets.QLabel(self.centralwidget)
        self.deltaLabel.setGeometry(QtCore.QRect(470, 210, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.deltaLabel.setFont(font)
        self.deltaLabel.setStyleSheet("color:rgb(255,255,255)")
        self.deltaLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.deltaLabel.setObjectName("deltaLabel")
        self.LaptimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.LaptimeLabel.setGeometry(QtCore.QRect(470, 120, 231, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.LaptimeLabel.setFont(font)
        self.LaptimeLabel.setStyleSheet("color:rgb(255,255,255)")
        self.LaptimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LaptimeLabel.setObjectName("LaptimeLabel")
        self.TC1Label = QtWidgets.QLabel(self.centralwidget)
        self.TC1Label.setGeometry(QtCore.QRect(15, 310, 73, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.TC1Label.setFont(font)
        self.TC1Label.setStyleSheet("color:rgb(255,255,255)")
        self.TC1Label.setAlignment(QtCore.Qt.AlignCenter)
        self.TC1Label.setObjectName("TC1Label")
        self.TC2Label = QtWidgets.QLabel(self.centralwidget)
        self.TC2Label.setGeometry(QtCore.QRect(101, 310, 73, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.TC2Label.setFont(font)
        self.TC2Label.setStyleSheet("color:rgb(255,255,255)")
        self.TC2Label.setAlignment(QtCore.Qt.AlignCenter)
        self.TC2Label.setObjectName("TC2Label")
        self.PFuelLabel = QtWidgets.QLabel(self.centralwidget)
        self.PFuelLabel.setGeometry(QtCore.QRect(15, 220, 127, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.PFuelLabel.setFont(font)
        self.PFuelLabel.setStyleSheet("color:rgb(255,255,255)")
        self.PFuelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PFuelLabel.setObjectName("PFuelLabel")
        self.revCounter = QtWidgets.QFrame(self.centralwidget)
        self.revCounter.setGeometry(QtCore.QRect(110, 26, 0, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.revCounter.sizePolicy().hasHeightForWidth())
        self.revCounter.setSizePolicy(sizePolicy)
        self.revCounter.setStyleSheet("color:rgb(255,255,255)")
        self.revCounter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.revCounter.setLineWidth(57)
        self.revCounter.setFrameShape(QtWidgets.QFrame.HLine)
        self.revCounter.setObjectName("revCounter")


    def runTasks(self):
            threadCount = QThreadPool.globalInstance().maxThreadCount()
            pool = QThreadPool.globalInstance()
            runnable = Runnable()
            pool.start(runnable)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.runTasks()
    MainWindow.show()
    sys.exit(app.exec_())
