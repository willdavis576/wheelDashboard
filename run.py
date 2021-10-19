# from PyQt5.QtWidgets import QApplication, QMainWindow
# import sys


# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setGeometry(0, 0, 720, 720)
#         self.setWindowTitle("PyQt5 window")
#         self.show()


# app = QApplication(sys.argv)
# window = Window()
# sys.exit(app.exec_())


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.setGeometry(0,0,720,720)
window.show()
app.exec()