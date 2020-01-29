##############################################
##	Used to recive requests and store into stacks while processed

import socket
import data_process as DATA_MODULE

class Host():

	def __init__(self):
		self._PORT = 3000
		self._BUFFER_LENGTH = 128
		self._HOST = ""
		self._LISTEN_TIMES = 100

		self._PROCESS_ = DATA_MODULE.initialize()
		self.init_server()

	def init_server(self):
		print('[INFO] Initializing Server', end=' ')

		try:
			_TIMES_LISTENED = 0
			soc = socket.socket(socket.AF_INET, socket.AF_INET, socket.SOCK_STREAM)
			soc.bind((self._HOST, self._PORT))
			print('Initialized')
			soc.listen(self._LISTEN_TIMES)
			while True:
				_TIMES_LISTENED += 1
				print('[SERVER] Listenning PORT ' + str(self._PORT))
				conn, addr = soc.accept()
				print('[SERVER] Request nº ' + str(_TIMES_LISTENED))
				print('[SERVER] Request from ' + str(addr))

				while True:
					rcData = conn.recv(self._BUFFER_LENGTH).decode()

					#######################################
					## PROCESS DATA RECIVED HERE
					print('[SERVER] Processing data.. ', end=' ')
					response = self._PROCESS_.process(rcData)
					print('finished')

					#######################################
					##	DATA RESPONSE
					print('[SERVER] Sending response ', end='')
					conn.send(response.encode())
					print('data sent')

		except Exception as e:
			print('[SERVER] ERROR ' + str(e))
		finally:
			print('[SERVER] Closing connection.. ', end='')
			soc.close()
			print('closed')

s = Host()