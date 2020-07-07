
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication, QVBoxLayout,QHBoxLayout, QPushButton
from PyQt5.QtCore import QThread, Qt, pyqtSignal
import sys
import time
import signal
from psutil import sensors_battery
from gtts import gTTS
import os
import time
import playsound



def make_sound(command):
    # frequency = 300
    # duration = 1400
    # Beep(frequency, duration)
    if command == "low":
        text = "Low battery. Please, plug in."
    else:
        text = "High battery. Risk of overcharging."

    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    playsound.playsound(filename)
    os.remove("voice.mp3")



if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MyThread(QThread):
        try:
            # Create a counter thread
            change_value = pyqtSignal(int)
            timeToSleep = pyqtSignal(int)
            def run(self):
                try:
                    cnt = 0
                    while True:
                        #cnt += 1
                        #print(cnt)
                        time.sleep(self.timeToSleep)
                        self.change_value.emit(cnt)
                except:
                    print("MyThread error")
        except: pass



class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Main window"
        self.top = App.primaryScreen().size().height()/3
        self.left = App.primaryScreen().size().width()/3
        w = 4
        h = 3.2
        self.width = App.primaryScreen().size().width()/w
        self.height = App.primaryScreen().size().height()/h
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        self.IS_ON = False

        self.lower_bound = 20
        self.upper_bound = 90

        self.batt = sensors_battery().percent

        Mainlayout = QVBoxLayout(self)

        labels = QHBoxLayout()
        label1 = QtWidgets.QLabel("Lower bound:")
        label2 = QtWidgets.QLabel("Upper bound:")
        labels.addWidget(label1)
        self.low = QtWidgets.QLineEdit()
        self.low.setText(str(self.lower_bound))
        self.low.setInputMask("99")
        labels.addWidget(self.low)
        labels.addWidget(label2)
        self.upp = QtWidgets.QLineEdit()
        self.upp.setText(str(self.upper_bound))
        self.upp.setInputMask("99")
        labels.addWidget(self.upp)
        Mainlayout.addLayout(labels)

        buttonlayout = QHBoxLayout()

        self.switchButton = QPushButton()
        self.switchButton.setStyleSheet("border-radius: 10px;")
        self.switchButton.setIcon(QtGui.QIcon('power-512.png'))
        self.switchButton.setIconSize(QtCore.QSize(150,150))
        self.switchButton.setFixedHeight(150)
        self.switchButton.setFixedWidth(150)
        buttonlayout.addWidget(self.switchButton)
        buttonlayout.setAlignment(Qt.AlignCenter)
        Mainlayout.addLayout(buttonlayout)

        batt_line = QHBoxLayout()
        batt_line.setAlignment(Qt.AlignCenter)
        batt_label = QtWidgets.QLabel(f"Battery Level {self.batt}%")
        batt_label.setFont(QtGui.QFont("Arial", 19, QtGui.QFont.Bold))
        batt_line.addWidget(batt_label)

        Mainlayout.addLayout(batt_line)


        self.switchButton.clicked.connect(lambda: switch())

        self.point = 50


        self.show()

        self.thread = MyThread()
        self.thread.timeToSleep = 10
        self.thread.change_value.connect(lambda : check())
        self.thread.start()




        def switch():
            if self.IS_ON == False:
                self.IS_ON = True
                self.low.setDisabled(True)
                self.upp.setDisabled(True)
                self.lower_bound = int(self.low.text())
                self.upper_bound = int(self.upp.text())
                self.switchButton.setIcon(QtGui.QIcon('on1.png'))
                self.switchButton.setIconSize(QtCore.QSize(150, 150))

            else:
                self.IS_ON = False
                self.low.setDisabled(False)
                self.upp.setDisabled(False)
                self.switchButton.setIcon(QtGui.QIcon('power-512.png'))
                self.switchButton.setIconSize(QtCore.QSize(150, 150))

        def check():
            battery = sensors_battery()
            plugged = battery.power_plugged
            percent = battery.percent
            batt_label.setText(f"Battery Level {percent}%")
            if self.IS_ON == False:
                return
            else:


                if plugged == False and percent <= self.lower_bound and abs(self.point - percent) >= 4:
                    self.point = percent
                    text = "Low battery. Please, plug in."
                    tts = gTTS(text=text, lang='en')
                    filename = 'voice.mp3'
                    tts.save(filename)
                    playsound.playsound(filename)
                   # playsound.playsound(filename)
                    os.remove("voice.mp3")


                if plugged == True and percent >= self.upper_bound and abs(self.point - percent) >= 3:
                    self.point = percent
                    text = "Risk of overcharging. Please, unplug."
                    tts = gTTS(text=text, lang='en')
                    filename = 'voice.mp3'
                    tts.save(filename)
                    playsound.playsound(filename)
                   # playsound.playsound(filename)
                    os.remove("voice.mp3")

    def closeEvent(self, event):

        print("Goodbye")
        self.thread.terminate()

        pid = os.getpid()
        os.kill(pid, signal.SIGINT)
        print(pid)
        print("BYE")





def runGUI():
    global App, window
    App = QApplication(sys.argv)
    App.setStyle('Fusion')
    window = MainWindow()
    sys.exit(App.exec())


if __name__ == '__main__':
        runGUI()
        App = QApplication(sys.argv)
        App.setStyle('Fusion')
        window = MainWindow()
        print("APP CLOSES")
        sys.exit(App.exec())

