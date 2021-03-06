import sys
import numpy as numpy
import _thread
import socket
import time

#pyqt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, QLineEdit, QWidget, QLabel, QGridLayout, QRadioButton, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPen, QIntValidator

sys.path.append('utils/')
import data

class App(QMainWindow):

	def __init__(self):
		super().__init__()

		#################################################
		##	STATIC VAR
		self._data_ = data.Data()
		self.pixmap = QPixmap(self._data_.get_pixmap())
		self.title = self._data_.get_title()
		self.LEFT = self._data_.get_left()
		self.TOP = self._data_.get_top()
		self.WIDTH = self._data_.get_width()
		self.HEIGHT = self._data_.get_height()
		

		#################################################
		##	TIMER
		self.flag_change = False
		self.SECONDS = 15
		self.ELAPSED = 0


		#################################################
		##	STATIC SERVER UTILS VAR
		self.invoice = self._data_.get_invoice()
		self.stock_code = self._data_.get_stock_code()
		self.quantity = self._data_.get_quantity()
		self.unit_price = self._data_.get_unit_price()
		self.customer_id = self._data_.get_customer_id()
		self.COUNTRY = self._data_.get_countrys()[0]

		##################################################
		##	RANDOMIZED FUNC SWITCH
		if self.COUNTRY == "France":
			self.RANDOM_PRODUCT = self._data_.get_french_product
		elif self.COUNTRY == "Portugal":
			self.RANDOM_PRODUCT = self._data_.get_portugease_product
		else:
			self.RANDOM_PRODUCT = self._data_.get_sweden_product

		#This local buffer retains information about all
		#user data
		self.local_buffer = list()
		#Anti-crashing flag
		self.user_flag = True

		#Screen button info
		self.local_buffer.append(self.RANDOM_PRODUCT())
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

		#This conditional will tell the button what to display
		self.ProductBtn = QPushButton(self.local_buffer[-1], self)


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

		#This conditional will acept action (or not)
		self.ProductBtn.clicked.connect(self.productAppAction)

	##	End of paint events
	######################################################

	## -------------------------------------------------#

	#####################################################
	##	NETWORK

	def start_connection(self):
		self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.soc.connect((self._data_.get_ip(), self._data_.get_port()))
		print("[NETWORK]\tStarted connection")

	def send_data(self, data):
		self.soc.send(data.encode())
		resp = self.soc.recv(self._data_.get_buffer_len())
		print("[NETWORK]\tResponse recived")
		return resp.decode()

	def kill_connection(self):
		self.soc.close()
		print("[NETWORK]\tClosed connection")

	##	End of NETWORK events
	######################################################

	## ------------------------------------------------- #

	######################################################
	##	UTILS

	def encode_data(self, data, flag, s = ""):
		#True  -> encodes buffer
		#False -> encodes all

		if flag:
			#buffer encoder uses $
			for i in range(len(data)):
				s += "$"+str(data[i])
		else:
			#simple encoder uses #
			for i in data:
				s += str(i) + "#"

		return s


	def mailer_thread(self, invoice, stock_code, quantity, unity_price, customer_id, country, ENCODED_STRING = ""):
		
		print("[+]\tNew thread is up")
		#Button Manipulation
		self.ProductBtn.setText("Waiting...")
		self.ProductBtn.setEnabled(False)
		self.update()

		self.start_connection()

		#Encoding information
		print("[THREAD]\tEncoding data")
		ENCODED_STRING += self.encode_data([invoice, stock_code, quantity, unity_price, customer_id, country], 0)
		ENCODED_STRING += self.encode_data(self.local_buffer, 1)
		self.flag_change = False

		#NETWORK
		print("[THREAD]\tSending data")
		resp = self.send_data(ENCODED_STRING)
		_thread.start_new_thread(self.counter_thread, (self.SECONDS,))

		if resp == 'reset':
			print("[THREAD]\tBuffer reset command recived")
			self.flag_change = True
			#If resp == reset, restart apriori function
			self.local_buffer = list()
			self.local_buffer.append(self.RANDOM_PRODUCT())
		else:
			self.local_buffer.append(str(resp))		#Storing response to local buffer
			self._data_.add_to_buffer(str(resp))	#Storing response to data buffer

		print("[-]\tThread is down")
		self.ProductBtn.setText(self.local_buffer[-1])
		self.ProductBtn.setEnabled(True)
		self.update()
		self.soc.close()

	def counter_thread(self, seconds):
		self.ELAPSED = 0
		while self.ELAPSED < seconds:
			time.sleep(1)

			if self.flag_change:
				self.ELAPSED = 0
				return

			print("Elapsed time: " + str(self.ELAPSED + 1))
			self.ELAPSED += 1

		#If @seconds passed:
		self.ELAPSED = 0	#Reset elapsed time
		if self.flag_change:
			return 			#Do nothing
		else:
			self.flag_change = True
			self.ProductBtn.setText(self.RANDOM_PRODUCT())	#Next product index for France, Sweden or Portugal
			self.update()


	######################################################
	##	Python slots
	@pyqtSlot()
	def productAppAction(self):
		_thread.start_new_thread(self.mailer_thread, (self.invoice, self.stock_code, self.quantity, self.unit_price, self.customer_id, self.COUNTRY) )

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.resize(ex.pixmap.width(), ex.pixmap.height())
	ex.move(500, 500)
	ex.setFixedSize(ex.size())
	ex.update()
	sys.exit(app.exec_())