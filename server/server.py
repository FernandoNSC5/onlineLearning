################################################
##	Used to recive requests and store into stacks while processed

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
	def new_client(self, client_socket, addr):
		while True:
			data = client_socket.recv(self._BL).decode() #Reciving data

			rcData = self.decoder_data(data)
			# Now: Index 5 -> Country
			#	   Index 6 -> Buffer data

			#####################################
			##	Processing data recived
			if(rcData[5] == 'France'):
				response = self.apriori_french(rcData)
				client_socket.send(response.encode())

			elif(rcData[5] == 'Portugal'):
				response = self.apriori_portugal(rcData)
				client_socket.send(response.encode())

			elif(rcData[5] == 'Sweden'):
				response = self.apriori_swrden(rcData)
				client_socket.send(response.encode())

			else:
				response = ""
				client_socket.send(response.encode())
			
		client_socket.close() #Closing connection

	def core(self):

		print("[STARTING] Starting network services")
		self._S.bind((self._HOST, self._PORT))
		self._S.listen(self._LISTEN_TIMES)

		print("[STARTED] Waiting connections")
		while True:
			c, addr = self._S.accept()
			print("[+] Creating THREAD connection")
			_thread.start_new_thread(self.new_client, (c, addr))
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

		#Adding everything to a unique var
		r = list()
		for i in range(len(data)-1):
			r.append(data[i])
		r.append(buffer_)

		return r

	## INIT APRIORI SEC
	def apriori_french(self, data):	#FRENCH METHOD
		# 5 -> país
		# 6 -> Buffer dados

		antecedents = data[6] # 6 -> Buffer de dados

		#Getting model and consequents
		french = self._PROCESS.get_french_model()
		french_antecedents = french['antecedents']
		french_consequents = french['consequents']

		#Adding to buffer queue
		self.add_customer_data(data)

		product = data[2] # 2 -> description or product name

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

		#Searching for results
		index = 0
		consequent = None #Consequent list to return
		for i in n_a:
			if i[0] == product:
				consequent = list(n_c[index])
				break
			index += 1

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if consequent == None:
			return ""
		else:
			return str(consequent[0])

	def apriori_portugal(self, data):	#PORTUGEASE METHOD
		
		product = data[2] # 2 -> description or product name

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
			if i[0] == product:
				consequent = list(n_c[index])
				break
			index += 1

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if consequent == None:
			return ""
		else:
			return str(consequent[0])

	def apriori_sweden(self, data):	#SWEDEN METHOD
		
		product = data[2] # 2 -> description or product name

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
			if i[0] == product:
				consequent = list(n_c[index])
				break
			index += 1

		############################################
		##	Parse list to string in order
		## 	to byte-encode it
		if consequent == None:
			return ""
		else:
			return str(consequent[0])

s = Server()