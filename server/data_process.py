# -*- coding: utf-8 -*-
import numpy as np
import sys
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

class Data():

	def __init__(self):
		print('Starting... ', end='')
		self.data = pd.read_excel('Online_retail.xlsx')
		self.data.head()
		self.data.columns
		self.data.Country.unique()
		print('Working')

		self.clean_data()
		self.unpatching_region()

	def encode(x):
		if x <= 0:
			return 0
		if x >= 1:
			return 1

	def clean_data(self):
		print('Cleaning data', end='.')
		#strip -> removes \n, \t, etc from strings
		self.data['Description'] = self.data['Description'].str.strip()
		print('.', end='')
		#Drops missing values (nulls, numpy nan)
		self.data.dropna(axis = 0 , subset = ['InvoiceNo'], inplace = True)
		print('.', end='')
		self.data['InvoiceNo'] = self.data['InvoiceNo'].astype('str')
		self.data = self.data[~self.data['InvoiceNo'].str.contains('C')]
		print('Done')

	def unpatching_region(self):
		print('unpatching.', end='')
		basket_France = (self.data[self.data['Country'] =="France"] 
		          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
		          .sum().unstack().reset_index().fillna(0) 
		          .set_index('InvoiceNo')) 
		  
		basket_UK = (self.data[self.data['Country'] =="United Kingdom"] 
		          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
		          .sum().unstack().reset_index().fillna(0) 
		          .set_index('InvoiceNo')) 
		  
		basket_Por = (self.data[self.data['Country'] =="Portugal"] 
		          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
		          .sum().unstack().reset_index().fillna(0) 
		          .set_index('InvoiceNo')) 
		  
		basket_Sweden = (self.data[self.data['Country'] =="Sweden"] 
		          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
		          .sum().unstack().reset_index().fillna(0) 
		          .set_index('InvoiceNo')) 
		print(' finished')
	

d = Data()