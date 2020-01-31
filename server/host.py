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

	#########################################################################
	##	METHODS	
	def add_customer_data(self, invoice, stock_code, description, quantity, unit_price, customer_id, country):
		_PROCESS_.add_customer_data(invoice, stock_code, description, quantity, unit_price, customer_id, country)

	def apriori_french(self, data):
		### Data must be in format list() with sequence of products selected 
		french = d.get_french_model()
		french_antecedents = french['antecedents']
		french_consequents = french['consequents']

		n_consequents = list()
		n_antecedents = list()

		for i in french_consequents:
			n_consequents.append(list(i))
		french_consequents = n_consequents

		for i in french_antecedents:
			n_antecedents.append(list(i))
		french_antecedents = n_antecedents

		for i in range(len(n_antecedents)):
			if data == n_antecedents[i]:
				return n_consequents[i]

		return None

	def apriori_portugal(self, data):
		### Data must be in format list() with sequence of products selected 
		portugal = d.get_portugease_model()
		portugal_antecedents = portugal['antecedents']
		portugal_consequents = portugal['consequents']

		n_consequents = list()
		n_antecedents = list()

		for i in portugal_consequents:
			n_consequents.append(list(i))
		portugal_consequents = n_consequents

		for i in portugal_antecedents:
			n_antecedents.append(list(i))
		portugal_antecedents = n_antecedents

		for i in range(len(n_antecedents)):
			if data == n_antecedents[i]:
				return n_consequents[i]

		return None

	def apriori_sweden(self, data):
		### Data must be in format list() with sequence of products selected 
		sweden = d.get_sweeden_model()
		sweden_antecedents = sweden['antecedents']
		sweden_consequents = sweden['consequents']

		n_consequents = list()
		n_antecedents = list()

		for i in sweden_consequents:
			n_consequents.append(list(i))
		sweden_consequents = n_consequents

		for i in sweden_antecedents:
			n_antecedents.append(list(i))
		sweden_antecedents = n_antecedents

		for i in range(len(n_antecedents)):
			if data == n_antecedents[i]:
				return n_consequents[i]

		return None

s = Host()