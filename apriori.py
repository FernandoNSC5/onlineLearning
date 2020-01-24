# -*- coding: utf-8 -*-

import numpy as np
import sys
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

print('Starting')

####################################################
##
##	Variables
data = pd.read_excel('Online_retail.xlsx') 
data.head() 
data.columns 
data.Country.unique() 

#####################################################
##
##	FUNCTIONS
def encode(x):
	if x<=0:
		return 0
	if x>=1:
		return 1

##
##	END OF FUNCTIONS
#####################################################

#####################################################
##
##	Limpando dados
print('Cleaning data.')
data['Description'] = data['Description'].str.strip()
data.dropna(axis = 0, subset =['InvoiceNo'], inplace = True) 
data['InvoiceNo'] = data['InvoiceNo'].astype('str')
data = data[~data['InvoiceNo'].str.contains('C')] 
##
##	Fim da limpeza
#####################################################

#####################################################
##
##	Segregando por região
print('unpatching.', end='')
basket_France = (data[data['Country'] =="France"] 
          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 
  
basket_UK = (data[data['Country'] =="United Kingdom"] 
          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 
  
basket_Por = (data[data['Country'] =="Portugal"] 
          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 
  
basket_Sweden = (data[data['Country'] =="Sweden"] 
          .groupby(['InvoiceNo', 'Description'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 
print(' finished')
##
##	Fim da segregação por região
######################################################

######################################################
##
##	Conversão de dados
print('Encoding.', end='')
basket_encoded = basket_France.applymap(encode) 
basket_France = basket_encoded 
  
basket_encoded = basket_UK.applymap(encode) 
basket_UK = basket_encoded 
  
basket_encoded = basket_Por.applymap(encode) 
basket_Por = basket_encoded 
  
basket_encoded = basket_Sweden.applymap(encode) 
basket_Sweden = basket_encoded 
print(' finished')
##
##	Fim de conversão
#######################################################

#######################################################
##
##	Criando modelos

###########	FRANCE ###############
frq_items = apriori(basket_France, min_support = 0.05, use_colnames = True) 
  
rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
print(rules.head())