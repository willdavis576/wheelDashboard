from PyQt5 import QtCore, QtGui, QtWidgets
import sys, time
from socket import *
from struct import *
from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from telemetry_f1_2021.listener import TelemetryListener

device = 1
backgroundLocation = ""
winBackLoc = "background-image: url(C:/Users/Will/OneDrive - Middlesex University/Inventions/fanatec wheel/wheelDashboard/mercDashBare.png); background-repeat: no-repeat; background-position: center;"
piBackLoc = "background-image: url(/home/pi/wheelDashboard/mercDashBare.png)"


if device == 0:
    backgroundLocation = winBackLoc
if device == 1:
    backgroundLocation = piBackLoc
    
class Runnable(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        self.initialiseUDPCon()

        while True:
                self.packet = self.listener.get()
                self.packet = {k: self.packet.get_value(k) for k, _ in self.packet._fields_}
                
                self.carTelem = self.packet.get('m_car_telemetry_data')
                if self.carTelem != None:
                        self.wheelData["speed"] = self.carTelem[19]['m_speed']
                        self.wheelData["gear"] = self.carTelem[19]['m_gear']
                        self.wheelData["rpm"] = self.carTelem[19]['m_engine_rpm']
                        self.wheelData["brake"] = self.carTelem[19]['m_brakes_temperature']
                        self.wheelData["tyre"] = self.carTelem[19]['m_tyres_inner_temperature']
                        print(self.wheelData)
                
                self.engineRPMScaled = round((self.wheelData["rpm"]) * (595 / 11000))
                ui.revCounter.setFixedWidth(self.engineRPMScaled)
                ui.revCounter.setLineWidth(self.engineRPMScaled)
                try:
                        ui.frontLeftBLabel.setText(str(self.wheelData["brake"][2]))
                        ui.frontRightBLabel.setText(str(self.wheelData["brake"][3]))
                        ui.backLeftBLabel.setText(str(self.wheelData["brake"][0]))
                        ui.backRightBlabel.setText(str(self.wheelData["brake"][1]))
                        
                        ui.frontLeftTLabel.setText(str(self.wheelData["tyre"][2]))
                        ui.frontRightTLabel.setText(str(self.wheelData["tyre"][3]))
                        ui.rearLeftTLabel.setText(str(self.wheelData["tyre"][0]))
                        ui.rearRightTLabel.setText(str(self.wheelData["tyre"][1]))
                except:
                        pass

                if (self.wheelData["gear"] > 0):
                        self.gearFinal = self.wheelData["gear"]

                if (self.wheelData["gear"] == 0):
                        self.gearFinal = "N"

                if (self.wheelData["gear"] == -1):
                        self.gearFinal = "R"

                self.speedFinal = self.wheelData["speed"]

                ui.gearLabel.setText(str(self.gearFinal))
                ui.speed.setText(str(self.speedFinal))

                
                
    def initialiseUDPCon(self):
        self.listener = TelemetryListener(port=20777, host='')
        self.wheelData = {"speed" : 0, "gear" : 0, "delta" : 0, "lastLapTime" : 0, "tyre" : [], "brake" : [], "rpm" : 0 }
        self.packet = ""
        self.carTelem = ""
        self.gearFinal = ""
        self.speedfinal = ""
        self.engineRPMScaled = ""
        self.constant = ""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(720, 720)
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
        self.gearLabel = QtWidgets.QLabel(self.centralwidget)
        self.gearLabel.setGeometry(QtCore.QRect(285, 81, 141, 170))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(140)
        font.setBold(True)
        font.setWeight(75)
        self.gearLabel.setFont(font)
        self.gearLabel.setStyleSheet("color:rgb(255,255,255)\n"
"")
        self.gearLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gearLabel.setObjectName("gearLabel")
        self.brakeBLabel = QtWidgets.QLabel(self.centralwidget)
        self.brakeBLabel.setGeometry(QtCore.QRect(430, 85, 281, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.brakeBLabel.setFont(font)
        self.brakeBLabel.setStyleSheet("color:rgb(255,255,255)\n"
"")
        self.brakeBLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.brakeBLabel.setObjectName("brakeBLabel")
        self.deltaLabel = QtWidgets.QLabel(self.centralwidget)
        self.deltaLabel.setGeometry(QtCore.QRect(0, 80, 281, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.deltaLabel.setFont(font)
        self.deltaLabel.setStyleSheet("color:rgb(255,255,255)")
        self.deltaLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.deltaLabel.setObjectName("deltaLabel")
        self.LaptimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.LaptimeLabel.setGeometry(QtCore.QRect(0, 170, 281, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.LaptimeLabel.setFont(font)
        self.LaptimeLabel.setStyleSheet("color:rgb(255,255,255)")
        self.LaptimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LaptimeLabel.setObjectName("LaptimeLabel")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 380, 720, 1))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frontLeftBLabel = QtWidgets.QLabel(self.centralwidget)
        self.frontLeftBLabel.setGeometry(QtCore.QRect(0, 250, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.frontLeftBLabel.setFont(font)
        self.frontLeftBLabel.setStyleSheet("color:rgb(255,255,255)")
        self.frontLeftBLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.frontLeftBLabel.setObjectName("frontLeftBLabel")
        self.frontRightBLabel = QtWidgets.QLabel(self.centralwidget)
        self.frontRightBLabel.setGeometry(QtCore.QRect(140, 250, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.frontRightBLabel.setFont(font)
        self.frontRightBLabel.setStyleSheet("color:rgb(255,255,255)")
        self.frontRightBLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.frontRightBLabel.setObjectName("frontRightBLabel")
        self.backLeftBLabel = QtWidgets.QLabel(self.centralwidget)
        self.backLeftBLabel.setGeometry(QtCore.QRect(0, 330, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.backLeftBLabel.setFont(font)
        self.backLeftBLabel.setStyleSheet("color:rgb(255,255,255)")
        self.backLeftBLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.backLeftBLabel.setObjectName("backLeftBLabel")
        self.backRightBlabel = QtWidgets.QLabel(self.centralwidget)
        self.backRightBlabel.setGeometry(QtCore.QRect(140, 330, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.backRightBlabel.setFont(font)
        self.backRightBlabel.setStyleSheet("color:rgb(255,255,255)")
        self.backRightBlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.backRightBlabel.setObjectName("backRightBlabel")
        self.frontLeftTLabel = QtWidgets.QLabel(self.centralwidget)
        self.frontLeftTLabel.setGeometry(QtCore.QRect(430, 250, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.frontLeftTLabel.setFont(font)
        self.frontLeftTLabel.setStyleSheet("color:rgb(255,255,255)")
        self.frontLeftTLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.frontLeftTLabel.setObjectName("frontLeftTLabel")
        self.frontRightTLabel = QtWidgets.QLabel(self.centralwidget)
        self.frontRightTLabel.setGeometry(QtCore.QRect(570, 250, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.frontRightTLabel.setFont(font)
        self.frontRightTLabel.setStyleSheet("color:rgb(255,255,255)")
        self.frontRightTLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.frontRightTLabel.setObjectName("frontRightTLabel")
        self.rearLeftTLabel = QtWidgets.QLabel(self.centralwidget)
        self.rearLeftTLabel.setGeometry(QtCore.QRect(430, 330, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.rearLeftTLabel.setFont(font)
        self.rearLeftTLabel.setStyleSheet("color:rgb(255,255,255)")
        self.rearLeftTLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rearLeftTLabel.setObjectName("rearLeftTLabel")
        self.rearRightTLabel = QtWidgets.QLabel(self.centralwidget)
        self.rearRightTLabel.setGeometry(QtCore.QRect(570, 330, 145, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.rearRightTLabel.setFont(font)
        self.rearRightTLabel.setStyleSheet("color:rgb(255,255,255)")
        self.rearRightTLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rearRightTLabel.setObjectName("rearRightTLabel")
        self.speed = QtWidgets.QLabel(self.centralwidget)
        self.speed.setGeometry(QtCore.QRect(430, 170, 281, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.speed.setFont(font)
        self.speed.setStyleSheet("color:rgb(255,255,255)\n"
"")
        self.speed.setAlignment(QtCore.Qt.AlignCenter)
        self.speed.setObjectName("speed")
        self.revCounter = QtWidgets.QFrame(self.centralwidget)
        self.revCounter.setGeometry(QtCore.QRect(0, 0, 100, 41))
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gearLabel.setText(_translate("MainWindow", "N"))
        self.brakeBLabel.setText(_translate("MainWindow", "60"))
        self.deltaLabel.setText(_translate("MainWindow", "+0:00"))
        self.LaptimeLabel.setText(_translate("MainWindow", "00:00"))
        self.frontLeftBLabel.setText(_translate("MainWindow", "100"))
        self.frontRightBLabel.setText(_translate("MainWindow", "100"))
        self.backLeftBLabel.setText(_translate("MainWindow", "100"))
        self.backRightBlabel.setText(_translate("MainWindow", "100"))
        self.frontLeftTLabel.setText(_translate("MainWindow", "100"))
        self.frontRightTLabel.setText(_translate("MainWindow", "100"))
        self.rearLeftTLabel.setText(_translate("MainWindow", "100"))
        self.rearRightTLabel.setText(_translate("MainWindow", "100"))
        self.speed.setText(_translate("MainWindow", "0"))
        
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
