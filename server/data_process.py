# -*- coding: utf-8 -*-

import numpy as np
import sys
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
sys.path.append('utils/')
import xls_utils as utils

class Data():

	def __init__(self):
		#####################################################
		##	UTILS
		_UTILS = utils.xls_utils()

		######################################################
		##	A.I PROCESS
		print('[STARTING]\tLoading data')
		self.data = pd.read_excel('Online_retail.xlsx') 
		self.data.head() 
		self.data.columns 
		self.data.Country.unique()
		print('[LOADED]\tCleaning data') 
		self.clean_data()
		print('[DATA CLEANED]\tRegion segmentation')
		self.region_seg()
		print('[SEGMENTED]\tEncoding')
		self.encoding()
		print('[ENCODED]\tCreating models')

		#####################################################
		##	MODELING
		self.french_models = self.create_french_models()
		self.portugease_models = self.create_portugease_models()
		self.sweedish_models = self.create_sweedish_moels()

		print('[MODELS READY]\n')

	def add_customer_data(self, invoice, stock_code, description, quantity, unit_price, customer_id, country):
		_UTILS.add_customer_data(invoice, stock_code, description, quantity, unit_price, customer_id, country)

	def update_data(self):
		print('[UPDATING DATA]\tWriting buffer to database')
		_UTILS.write_xls()
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
		self.french_models = self.create_french_models()
		self.portugease_models = self.create_portugease_models()
		self.sweedish_models = self.create_sweedish_moels()

		print('[NEW MODELS READY]\n')

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
		return rules.head()

	def create_portugease_models(self):
		frq_items = apriori(self.portugal_balance, min_support = 0.05, use_colnames = True)   
		rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
		rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
		return rules.head()

	def create_sweedish_moels(self):
		frq_items = apriori(self.sweden_balance, min_support = 0.05, use_colnames = True)   
		rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
		rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
		return rules.head()

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

	def get_sweeden_model(self):
		return self.sweedish_models
