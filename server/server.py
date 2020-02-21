################################################
##	Used to recive requests and store into stacks while processed

import random
import socket
import _thread
import data_process
import colorama

class Server():

	def __init__(self):
		colorama.init()
		self._FORE = colorama.Fore

		print(self._FORE.CYAN + "[STARTING]\t" + self._FORE.RESET + " Initializing core variables")
		self._S = socket.socket()
		self._HOST = ''
		self._PORT = 3000
		self._BL = 128
		self._LISTEN_TIMES = 100

		print(self._FORE.CYAN + "[INITIALIZED]\t" + self._FORE.RESET + " Calling data module")
		self._PROCESS = data_process.Data()
		print(self._FORE.CYAN + "[SERVER]\t" + self._FORE.RESET + " Ready")
		print()

		self.core() #Initializing system

	############################################
	##	NETWORK Methods
	def new_client(self, client_socket, addr, counter_conn):
		while True:
			
			data = client_socket.recv(self._BL).decode() #Reciving data
			if data == '' or len(data) == 0:
				continue

			rcData = self.decoder_data(data)
			# Now: Index 5 -> Country
			#	   Index 6 -> Buffer data

			#####################################
			##	Processing data recived
			if(rcData[5] == 'France'):
				print(self._FORE.MAGENTA + "[SERVER]\t" + self._FORE.RESET + " France selected")
				response = self.apriori_french(rcData)
				client_socket.send(response.encode())

			elif(rcData[5] == 'Portugal'):
				print(self._FORE.MAGENTA + "[SERVER]\t" + self._FORE.RESET + " Portugal selected")
				response = self.apriori_portugal(rcData)
				client_socket.send(response.encode())

			elif(rcData[5] == 'Sweden'):
				print(self._FORE.MAGENTA + "[SERVER]\t" + self._FORE.RESET + " Sweden selected")
				response = self.apriori_sweden(rcData)
				client_socket.send(response.encode())

			else:
				print(self._FORE.RED + "[SERVER] Nothing selected" + self._FORE.RESET)
				response = ""
				client_socket.send(response.encode())

			#Writes buffer to xlsx every 5 requests
			if counter_conn % 5 == 0:
				self._PROCESS.print_buffer_data()
				self._PROCESS.update_data()
			
		client_socket.close() #Closing connection

	def core(self):

		print(self._FORE.CYAN + "[STARTING]\t" + self._FORE.RESET + " Starting network services")
		self._S.bind((self._HOST, self._PORT))
		self._S.listen(self._LISTEN_TIMES)
		counter = 0

		print(self._FORE.CYAN + "[STARTED]\t" + self._FORE.RESET + " Waiting connections")
		while True:
			c, addr = self._S.accept()
			counter += 1
			print(self._FORE.BLUE + "[+]\t\t" + self._FORE.RESET + " Creating THREAD connection")
			_thread.start_new_thread(self.new_client, (c, addr, counter))
		self._S.close()

	##	End of NETWORK Methods
	################################################

	#----------------------------------------------#

	################################################
	##	Methods
	################################################

	#BASICS
	def add_customer_data(self, data):
		for i in data[6]:
			self._PROCESS.add_customer_data(data[0], data[1], data[2], data[3], data[4], data[5], i)

	def decoder_data(self, data):
		#Converting to list
		aux = data.split('#')
		buffer_ = aux[6].split('$')
		
		#Cleanning buffer
		_buffer_ = list()
		for i in buffer_:
			if i != '':
				_buffer_.append(i)
		buffer_ = _buffer_

		#Adding everything to a unique var
		r = list()
		counter = 0
		for i in aux:
			if counter == 6:
				break
			r.append(i)
			counter += 1
		r.append(buffer_)

		return r

	## INIT APRIORI SEC
	def apriori_french(self, data):	#FRENCH METHOD

		#Hash module
		HASHER = lambda x : hash(tuple(set(x)))

		antecedents = data[6] # 6 -> Buffer de dados

		#Cleanning buffer
		for i in range(len(antecedents)):
			antecedents[i] = antecedents[i].strip()

		antecedents_h = HASHER(antecedents) #hashs antecedent data

		#Getting model and consequents
		french = self._PROCESS.get_french_model()
		french_antecedents = french['antecedents']
		french_consequents = french['consequents']

		#Adding to buffer queue
		self.add_customer_data(data)

		n_c = list()
		n_a = list()

		#Converting frozen-set to list
		for i in french_antecedents:
			n_a.append(HASHER(i))
		for i in french_consequents:
			n_c.append(list(i))

		#Searching for results
		r = list()
		for i in range(len(n_a)):
			if n_a[i] == antecedents_h:
				r.append(n_c[i])

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if len(r):
			r = r[0]
			return r[0]
		else:
			return "reset"

	def apriori_portugal(self, data):	#PORTUGEASE METHOD

		#Hash module
		HASHER = lambda x : hash(tuple(set(x)))
		
		antecedents = data[6] # 6 -> Buffer de dados

		#Cleanning buffer
		for i in range(len(antecedents)):
			antecedents[i] = antecedents[i].strip()

		antecedents_h - HASHER(antecedents)

		#Getting model and consequents
		portugal = self._PROCESS.get_portugease_model()
		portugal_antecedents = portugal['antecedents']
		portugal_consequents = portugal['consequents']

		#Adding to buffer queue
		self.add_customer_data(data)

		n_c = list()
		n_a = list()

		#Converting frozen-set to list
		for i in portugal_antecedents:
			n_a.append(HASHER(i))
		for i in portugal_consequents:
			n_c.append(list(i))

		n_c = self.n_cleaner(n_c, antecedents)

		#Searching for results
		r = list()
		for i in range(len(n_a)):
			if n_a[i] == antecedents_h:
				r.append(n_c[i])

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if len(r):
			r = r[0]
			return r[0]
		else:
			return "reset"

	def apriori_sweden(self, data):	#SWEDEN METHOD

		#Hash module
		HASHER = lambda x : hash(tuple(set(x)))
		
		antecedents = data[6] # 6 -> Buffer de dados
		
		#Cleanning buffer
		for i in range(len(antecedents)):
			antecedents[i] = antecedents[i].strip()

		antecedents_h = HASHER(antecedents)

		#Getting model and consequents
		sweden = self._PROCESS.get_sweden_model()
		sweden_antecedents = sweden['antecedents']
		sweden_consequents = sweden['consequents']

		#Adding to buffer queue
		self.add_customer_data(data)

		n_c = list()
		n_a = list()

		#Converting frozen-set to list
		for i in sweden_antecedents:
			n_a.append(HASHER(i))
		for i in sweden_consequents:
			n_c.append(list(i))

		n_c = self.n_cleaner(n_c, antecedents)

		#Searching for results
		r = list()
		for i in range(len(n_a)):
			if n_a[i] == antecedents_h:
				r.append(n_c[i])

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if len(r):
			r = r[0]
			return r[0]
		else:
			return "reset"

s = Server()