################################################
##	Used to recive requests and store into stacks while processed

import random
import socket
import _thread
import data_process

class Server():

	def __init__(self):
		print("[STARTING] Initializing core variables")
		self._S = socket.socket()
		self._HOST = ''
		self._PORT = 3000
		self._BL = 128
		self._LISTEN_TIMES = 100

		print("[INITIALIZED] Calling data module")
		self._PROCESS = data_process.Data()
		print("[SERVER] Ready")
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
				print("[SERVER] France selected")
				response = self.apriori_french(rcData)
				client_socket.send(response.encode())

			elif(rcData[5] == 'Portugal'):
				print("[SERVER] Portugal selected")
				response = self.apriori_portugal(rcData)
				client_socket.send(response.encode())

			elif(rcData[5] == 'Sweden'):
				print("[SERVER] Sweden selected")
				response = self.apriori_sweden(rcData)
				client_socket.send(response.encode())

			else:
				print("[SERVER] Nothing selected")
				response = ""
				client_socket.send(response.encode())

			if counter_conn % 5 == 0:
				print("[SERVER] On buffer:")
				self._PROCESS.print_buffer_data()
				self._PROCESS.update_data()
			
		client_socket.close() #Closing connection

	def core(self):

		print("[STARTING] Starting network services")
		self._S.bind((self._HOST, self._PORT))
		self._S.listen(self._LISTEN_TIMES)
		counter = 0

		print("[STARTED] Waiting connections")
		while True:
			c, addr = self._S.accept()
			counter += 1
			print("[+] Creating THREAD connection")
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

		antecedents = data[6] # 6 -> Buffer de dados

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
			n_a.append(list(i))
		for i in french_consequents:
			n_c.append(list(i))

		#Deleting antecedents from consequent list
		index = 0
		for i in n_c:
			for j in antecedents:
				if j in i:
					n_c[index].remove(j)
			index += 1

		#Searching for results
		index = 0
		consequent = None #Consequent list to return
		for i in n_a:
			if not len(set(i).intersection(antecedents)): 
				consequent = list(n_c[index])
				break
			index += 1

		print("Antecedents: " + str(antecedents))
		print("Consequents: " + str(consequent))

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if len(consequent):
			return consequent[0]
		else:
			return "reset"

	def apriori_portugal(self, data):	#PORTUGEASE METHOD
		
		antecedents = data[6] # 6 -> Buffer de dados

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
			n_a.append(list(i))
		for i in portugal_consequents:
			n_c.append(list(i))

		#Searching for results
		index = 0
		consequent = None #Consequent list to return
		for i in n_a:
			if not len(set(i).intersection(antecedents)): 
				consequent = list(n_c[index])
				break
			index += 1

		print("Antecedents: " + str(antecedents))
		print("Consequents: " + str(consequent))

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if consequent == None:
			return ""
		else:
			return str(consequent[0])

	def apriori_sweden(self, data):	#SWEDEN METHOD
		
		antecedents = data[6] # 6 -> Buffer de dados

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
			n_a.append(list(i))
		for i in sweden_consequents:
			n_c.append(list(i))

		#Searching for results
		index = 0
		consequent = None #Consequent list to return
		for i in n_a:
			if not len(set(i).intersection(antecedents)): 
				consequent = list(n_c[index])
				break
			index += 1

		print("Antecedents: " + str(antecedents))
		print("Consequents: " + str(consequent))

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if consequent == None:
			return ""
		else:
			return str(consequent[0])

s = Server()