# -*- coding: utf-8 -*-

import numpy as np
import sys
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
sys.path.append('utils/')
import xls_utils as utils
import threading
import colorama

class Data():

	def __init__(self):
		#####################################################
		##	UTILS
		colorama.init()
		self._FORE = colorama.Fore
		self._UTILS = utils.xls_utils()

		######################################################
		##	A.I PROCESS
		print(self._FORE.CYAN + '[STARTING]' + self._FORE.RESET + '\tLoading data')
		self.data = pd.read_excel('Online_retail.xlsx') 
		self.data.head() 
		self.data.columns 
		self.data.Country.unique()
		print(self._FORE.CYAN + '[LOADED]' + self._FORE.RESET + '\tCleaning data') 
		self.clean_data()
		print(self._FORE.CYAN + '[DATA CLEANED]' + self._FORE.RESET + '\tRegion segmentation')
		self.region_seg()
		print(self._FORE.CYAN + '[SEGMENTED]' + self._FORE.RESET + '\tEncoding')
		self.encoding()
		print(self._FORE.CYAN + '[ENCODED]' + self._FORE.RESET + '\tCreating models')

		#####################################################
		##	MODELING
		self.french_models = self.create_french_models()
		self.portugease_models = self.create_portugease_models()
		self.sweedish_models = self.create_sweedish_moels()

		print(self._FORE.CYAN + '[MODELS READY]\n' + self._FORE.RESET)

	def add_customer_data(self, invoice, stock_code, quantity, unit_price, customer_id, country, description):
		self._UTILS.add_customer_data(invoice, stock_code, quantity, unit_price, customer_id, country, description)

	def print_buffer_data(self):
		self._UTILS.print_buffer()

	def update_data(self):
		print(self._FORE.MAGENTA + "[THREADING]" + self._FORE.RESET + "\tPreparing to write data")
		thr = threading.Thread(target=self.update_data_slave, args=(), kwargs={})
		thr.start()

	def update_data_slave(self):
		print()
		print(self._FORE.RED + "===========================================")
		print('[UPDATING DATA]\tWriting buffer to database')
		print("===========================================" + self._FORE.RESET)
		self._UTILS.write_xls()
		print('[UPDATED]\tLoading new database')
		self.data = pd.read_excel('Online_retail.xlsx') 
		self.data.head() 
		self.data.columns 
		self.data.Country.unique()
		print('[RELOADED]\tCleaning data') 
		self.clean_data()
		print('[DATA CLEANED]\tRegion segmentation')
		self.region_seg()
		print('[RESEGMENTED]\tEncoding')
		self.encoding()
		print('[REENCODED]\tCreating models')
		self.gen_new_models()
		print("[FINISHED]")
		print(self._FORE.RED + "============================================" + self._FORE.RESET)

	def gen_new_models(self):
		self.french_models = self.create_french_models()
		self.portugease_models = self.create_portugease_models()
		self.sweedish_models = self.create_sweedish_moels()

		print(self._FORE.GREEN + '[NEW MODELS READY]\n' + self._FORE.RESET)

	def clean_data(self):
		self.data['Description'] = self.data['Description'].str.strip() #strip -> removes \n, \t, etc from strings
		self.data.dropna(axis = 0, subset =['InvoiceNo'], inplace = True) #Drops missing values (nulls, numpu nan) 
		self.data['InvoiceNo'] = self.data['InvoiceNo'].astype('str')
		self.data = self.data[~self.data['InvoiceNo'].str.contains('C')] 

	def region_seg(self):
		self.france_balance = (self.data[self.data['Country'] =="France"] 
		          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
		          .sum().unstack().reset_index().fillna(0) 
		          .set_index('InvoiceNo')) 
		  
		self.portugal_balance = (self.data[self.data['Country'] =="Portugal"] 
		          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
		          .sum().unstack().reset_index().fillna(0) 
		          .set_index('InvoiceNo')) 
		  
		self.sweden_balance = (self.data[self.data['Country'] =="Sweden"] 
		          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
		          .sum().unstack().reset_index().fillna(0) 
		          .set_index('InvoiceNo')) 

	def encoding(self):
		self.encoded_balance = self.france_balance.applymap(self.encode) 
		self.france_balance = self.encoded_balance 
		  
		self.encoded_balance = self.portugal_balance.applymap(self.encode) 
		self.portugal_balance = self.encoded_balance 
		  
		self.encoded_balance = self.sweden_balance.applymap(self.encode) 
		self.sweden_balance = self.encoded_balance 

	def create_french_models(self):
		frq_items = apriori(self.france_balance, min_support = 0.05, use_colnames = True)   
		rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
		rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
		return rules

	def create_portugease_models(self):
		frq_items = apriori(self.portugal_balance, min_support = 0.05, use_colnames = True)   
		rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
		rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
		return rules

	def create_sweedish_moels(self):
		frq_items = apriori(self.sweden_balance, min_support = 0.05, use_colnames = True)   
		rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
		rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
		return rules

	def encode(self, x):
		if x<=0:
			return 0
		if x>=1:
			return 1


	########################################################################
	##	GETTERS AND SETTERS

	def get_french_model(self):
		return self.french_models

	def get_portugease_model(self):
		return self.portugease_models

	def get_sweden_model(self):
		return self.sweedish_models
