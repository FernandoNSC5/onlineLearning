class Data():

	def __init__(self):

		###########################
		##	WEB
		self._IP_ = '192.168.0.1'
		self._PORT_ = 3333
		self._BUFFER_LENGHT_ = 128
		self._HOST_NAME_ = ""

		###########################
		##	UI
		self._TITLE_ = "Apriori V0.2"
		self._PIXMAP_ = "../src/background.png"
		self._LEFT_ = 10
		self._TOP_ = 10
		self._WIDTH_ = 800
		self._HEIGHT_ = 600

		############################
		## Hardcoded products
		self._COUNTRYS_ = ['France', 'Portugal', 'Sweden']
		self._PRODUCTS_ = list()

	##################################################
	##	Getters
	#web
	def get_ip(self):
		return self._IP_

	def get_port(self):
		return self._PORT_

	def get_buffer_len(self):
		return self._BUFFER_LENGHT_

	def get_host_name(self):
		return self._HOST_NAME_

	#ui
	def get_title(self):
		return self._TITLE_

	def get_pixmap(self):
		return self._PIXMAP_

	def get_left(self):
		return self._LEFT_

	def get_top(self):
		return self._TOP_

	def get_width(self):
		return self._WIDTH_

	def get_height(self):
		return self._HEIGHT_

	#products list
	def get_countrys(self):
		return _COUNTRYS_

	def get_products(self):
		return _PRODUCTS_