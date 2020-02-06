import socket

class WEB_SERVICE():

	def __init__(self):
		self._IP = '' #SERVER IP
		self._PORT = '' #SERVER PORT
		self._BUFFER_LENGHT = 128

	#STARTING CONN
	def start(self):
		try:
			print('[INFO] Starting connection.. ', end='')
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.soc.connect((self._IP, self._PORT))
			print('working')
			return 'Ready'
		except Exception as e:
			print('[ERROR] ' + str(e))
			return 'Error, try again'

	def send_data(self, data):

		if data == None or data == "" or not data:
			print('[WARNING] Empty data')
			return 'ERROR'

		try:

			print('[INFO] Sending data.. ', end='')
			self.soc.send(data.encode())
			print('[INFO] Waiting for response')
			resp = self.soc.recv(self._BUFFER_LENGHT).decode()
			print('[INFO] Recived')
			return resp
		
		except Exception as e:
			print('[ERROR] ' + str(e))

		finally:
			self.soc.close()
			return
