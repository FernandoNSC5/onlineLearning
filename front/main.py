import sys
import asyncio
import time
import numpy as numpy

#pyqt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, QLineEdit, QWidget, QLabel, QGridLayout, QRadioButton, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPen, QIntValidator

sys.path.append('utils/')
import soc_front_use
import data

class App(QMainWindow):

	def __init__(self):
		super().__init__()

		#################################################
		##	STATIC VAR
		self._DATA_ = data.Data()
		self.pixmap = QPixmap(self._DATA_.get_pixmap())
		self.title = self._DATA_.get_title()
		self.LEFT = self._DATA_.get_left()
		self.TOP = self._DATA_.get_top()
		self.WIDTH = self._DATA_.get_width()
		self.HEIGHT = self._DATA_.get_height()
		self.LOCATIONS = self._DATA_.get_countrys()

		#Sockets usage
		_SOCKET_ = soc_front_use

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
		self.description = self._DATA_.get_randomized_product()
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

		country = LOCATIONS[0]
		invoice = 1234
		stock_code = 1234
		desc = self.description
		quantity = 1
		unit_price = 1.8
		customer_id = 59999

		_RESPONSE_ = _SOCKET_.send_data([invoice, stock_code, desc, quantity, unit_price, customer_id, country])
		return _RESPONSE_

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.resize(ex.pixmap.width(), ex.pixmap.height())
	ex.move(500, 500)
	ex.setFixedSize(ex.size())
	ex.update()
	sys.exit(app.exec_())