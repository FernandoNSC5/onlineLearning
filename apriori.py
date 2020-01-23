import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

#Loading data
print("Wait, reading data...")
data = pd.read_excel('Online_retail.xlsx')
data.head()
print("Data ready")

#Columns
print(data.columns)

#Regions
print(data.Country.unique())