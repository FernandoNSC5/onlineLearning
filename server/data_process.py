# -*- coding: utf-8 -*-
import numpy as np
import sys
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

class Data():

	def __init__(self):
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
		self.models = self.create_models()
		print('[MODELS READY]\n')
		print(self.models)

	def update_data(self):
		print('[UPDATING DATA]\t Reloading data')
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
		self.models = self.create_models()
		print('[NEW MODELS READY]\n')
		print(self.models)

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
		  
		self.uk_balance = (self.data[self.data['Country'] =="United Kingdom"] 
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
		  
		self.encoded_balance = self.uk_balance.applymap(self.encode) 
		self.uk_balance = self.encoded_balance 
		  
		self.encoded_balance = self.portugal_balance.applymap(self.encode) 
		self.portugal_balance = self.encoded_balance 
		  
		self.encoded_balance = self.sweden_balance.applymap(self.encode) 
		self.sweden_balance = self.encoded_balance 

	def create_models(self):

		frq_items = apriori(self.france_balance, min_support = 0.05, use_colnames = True)   
		rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
		rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
		_antecedents_ = rules.head()['antecedents']
		_consequents_ = rules.head()['consequents']
		_confidence_ = rules.head()['confidence']

		return rules.head()

	def encode(self, x):
		if x<=0:
			return 0
		if x>=1:
			return 1

d = Data()