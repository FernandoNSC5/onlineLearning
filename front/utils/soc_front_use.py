import socket

class WEB_SERVICE():

	def __init__(self, ip, port):
		self._IP = ip #SERVER IP
		self._PORT = port #SERVER PORT
		self._BUFFER_LENGHT = 128
		self.start()

	#STARTING CONN
	def start(self):
		try:
			print('[WEB SERVICE]\t Creating socket.. ')
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print('[UP]\t Connecting..')
			self.soc.connect((self._IP, self._PORT))
			print('[CONNECTED]')
			return 'Ready'
		except Exception as e:
			print(str(e))
			return 'Error, try again'

	def send_data(self, data):

		if data == None or data == "" or not data:
			print('[WARNING]\t Empty data')
			return 'ERROR'

		try:

			print('[INFO]\t Sending data.. ')
			print("Data: " + str(data))
			self.soc.send(str(data).encode())
			print('[INFO]\t Waiting for response')
			resp = self.soc.recv(self._BUFFER_LENGHT).decode()
			print('[INFO]\t Recived')
			return resp
		
		except Exception as e:
			print(str(e))

		finally:
			self.soc.close()
			return
