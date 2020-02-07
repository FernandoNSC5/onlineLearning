import sys
import asyncio
import time
import numpy as numpy

#pyqt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, QLineEdit, QWidget, QLabel, QGridLayout, QRadioButton, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPen, QIntValidator
from termcolor import colored

sys.path.append('utils/')
import soc_front_use
import data

class App(QMainWindow):

	def __init__(self):
		super().__init__()

		#################################################
		##	STATIC VAR
		print("[U.I.]\tStarting...")
		self._DATA_ = data.Data()
		self.pixmap = QPixmap(self._DATA_.get_pixmap())
		self.title = self._DATA_.get_title()
		self.LEFT = self._DATA_.get_left()
		self.TOP = self._DATA_.get_top()
		self.WIDTH = self._DATA_.get_width()
		self.HEIGHT = self._DATA_.get_height()
		self.LOCATIONS = self._DATA_.get_countrys()

		print("[U.I.]\tCalling socket ")
		#Sockets usage
		self._SOCKET_ = soc_front_use.WEB_SERVICE(self._DATA_.get_ip(), self._DATA_.get_port())

		print("[U.I.]\tCreating description")
		#Screen button info
		self.description = self._DATA_.get_randomized_product()

		print("[U.I.]\tBreaking windows flags")
		#Destroying Windows Flags
		self.setWindowFlags(
						QtCore.Qt.Window |
						QtCore.Qt.CustomizeWindowHint |
						QtCore.Qt.WindowTitleHint |
						QtCore.Qt.WindowCloseButtonHint |
						QtCore.Qt.WindowStaysOnTopHint
						)

		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT)

		#Draw product btn
		self.drawProductButton()

		self.show()
		print("[U.I.]\tup.")

	#####################################################
	##	Paint event
	def paintEvent(self, e):
		painter = QtGui.QPainter(self)
		painter.drawPixmap(self.rect(), self.pixmap)
		painter.setRenderHint(QPainter.Antialiasing, True)

		pen = QtGui.QPen()
		pen.setWidth(3)
		pen.setColor(QtCore.Qt.black)
		pen.setCapStyle(QtCore.Qt.RoundCap)
		pen.setJoinStyle(QtCore.Qt.RoundJoin)
		painter.setPen(pen)

	def drawProductButton(self):
		self.ProductBtn = QPushButton(self.description, self)
		self.ProductBtn.setVisible(True)
		self.ProductBtn.resize(490,120)
		self.ProductBtn.move(157,345)
		self.ProductBtn.setStyleSheet("QPushButton {background-color: #CAB8B2}"
				"QPushButton {color: white}"
				"QPushButton {border-radius: 12px}"
				"QPushButton {font-family: Calibri}"
				"QPushButton {font-size: 20px}"
				"QPushButton:hover {background-color: #a3867c}"
				"QPushButton:hover:!pressed {background-color: #6e5f5a}")
		self.ProductBtn.clicked.connect(self.productAppAction)

	def process_data(self, data):
		s = ""
		for i in data:
			s = s+str(i)
			s = s+"#"
		return s

	######################################################
	##	Python slots
	@pyqtSlot()
	def productAppAction(self):
		
		#########################
		##	DATA ORDER
		##	-invoice
		##	-stock_code
		##	-description
		##	-quantity
		##	-unit_price
		##	-customer_id
		##	-country

		print("[CLICKED]\t Started static variables")
		country = self.LOCATIONS[0]
		invoice = 1234
		stock_code = 1234
		desc = self.description
		quantity = 1
		unit_price = 1.8
		customer_id = 59999

		print("[STARTED]\t Sending data")
		_d = self.process_data([invoice, stock_code, desc, quantity, unit_price, customer_id, country])
		_RESPONSE_ = self._SOCKET_.send_data(_d)

		if "[ERROR]" in _RESPONSE_:
			print("An error ocurred on back-end")
			return

		print("[RECIVED] Apriori well runned")

		#New product - Apriori based
		self.description = _RESPONSE_[0]

		return _RESPONSE_

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.resize(ex.pixmap.width(), ex.pixmap.height())
	ex.move(500, 500)
	ex.setFixedSize(ex.size())
	ex.update()
	sys.exit(app.exec_())