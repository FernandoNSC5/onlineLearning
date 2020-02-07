##############################################
##	Used to recive requests and store into stacks while processed

import socket
import data_process as DATA_MODULE

class Host():

	def __init__(self):
		print("[STARTED]\t Initializing core variables")
		self._PORT = 3000
		self._BUFFER_LENGTH = 128
		self._HOST = ""
		self._LISTEN_TIMES = 100

		print("[INITIALIZED]\t Calling DATA MODULE\t")
		self._PROCESS_ = DATA_MODULE.Data()
		self.init_server()

	def init_server(self):

		try:
			err_flag = False
			_TIMES_LISTENED = 0
			soc = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
			soc.bind((self._HOST, self._PORT))
			print('Initialized')
			soc.listen(self._LISTEN_TIMES)
			while True:
				_TIMES_LISTENED += 1
				print('[SERVER]\t Listenning PORT ' + str(self._PORT))
				conn, addr = soc.accept()
				print('[SERVER]\t Request nº ' + str(_TIMES_LISTENED))
				print('[SERVER]\t Request from ' + str(addr))

				while True:
					rc_Data = conn.recv(self._BUFFER_LENGTH).decode()
					print("Recived: " + str(rc_Data))
					rcData = rc_Data.split('#')
					print("Processed: " + str(rcData))

					#######################################
					## PROCESS DATA RECIVED HERE
					print('[SERVER]\t Processing data.. ')
					#French processing data
					if(rcData[6] == 'France'):
						print("into france")
						try:
							response = self.apriori_french(rcData)
							print("response recived")
							print("Response: " + str(response))
							conn.send(response.encode())
						except Exception as e:
							print("[ERROR]\t" + str(e))
							conn.send(e.encode())

					#Portugal processing data
					if(rcData[6] == 'Portugal'):
						print("into portugal")
						try:
							response = self.apriori_portugal(rdData)
							conn.send(e.encode())
						except Exception as e:
							print("[ERROR]\t " + str(e))
							conn.send(e.encode())

					#Sweden processing data
					if(rcData[6] == 'Sweden'):
						print("into sweden")
						try:
							response = self.apriori_sweden(rcData)
							conn.send(e.encode())
						except Exception as e:
							print("[ERROR]\t " + str(e))
							conn.send(e.encode())

					else:
						#Error flag
						print("[ERROR] Returning NULL")
						err_flag = True
						conn.send("".encode())
						continue

					# XLS Data atualization
					#if _TIMES_LISTENED % 50 == 0:
					_PROCESS_.update_data()

					#response = self._PROCESS_.process(rcData)
					print('[FINISHED]')

					#######################################
					##	DATA RESPONSE
					print('[SERVER]\t Sending response ')
					conn.send(response.encode())
					print('[SENT]')

		except Exception as e:
			print(str(e))
			err_flag = True
		finally:
			print('[SERVER]\t Closing connection.. ')
			if not err_flag:
				soc.close()
			print('closed')

	#########################################################################
	##	METHODS	
	def add_customer_data(self, invoice, stock_code, description, quantity, unit_price, customer_id, country):
		self._PROCESS_.add_customer_data(invoice, stock_code, description, quantity, unit_price, customer_id, country)



	def apriori_french(self, data):
		print("[RUNNING]\t Apriori FRENCH MODEL")
		### Data must be in format list() with sequence of products selected
		french = self._PROCESS_.get_french_model()
		french_antecedents = french['antecedents']
		french_consequents = french['consequents']

		#Adding to write queue
		self.add_customer_data(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

		n_consequents = list()
		n_antecedents = list()

		for i in french_consequents:
			n_consequents.append(list(i))
		french_consequents = n_consequents


		for i in french_antecedents:
			n_antecedents.append(list(i))
		french_antecedents = n_antecedents

		print("\n\nRUNNING SEARCH")
		for i in range(len(n_antecedents)):
			print(str(n_antecedents[i]))
			if data == n_antecedents[i]:
				return n_consequents[i]

		return None

	def apriori_portugal(self, data):
		print("[RUNNING]\t Apriori PORTUGAL MODEL")
		### Data must be in format list() with sequence of products selected 
		portugal = self._PROCESS_.get_portugease_model()
		portugal_antecedents = portugal['antecedents']
		portugal_consequents = portugal['consequents']

		#Adding to write queue
		self.add_customer_data(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

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
		print("[RUNNING]\t Apriori SWEDEN MODEL")
		### Data must be in format list() with sequence of products selected 
		sweden = self._PROCESS_.get_sweeden_model()
		sweden_antecedents = sweden['antecedents']
		sweden_consequents = sweden['consequents']

		#Adding to write queue
		self.add_customer_data(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

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