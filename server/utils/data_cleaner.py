import pandas as pd
import numpy as np

##########################################################
##	Script created and used to delete any data from
##	countrys that not portugal, sweden or france
##

print("[STARTED]\t loading base")
data = pd.read_excel('../Online_retail.xlsx')
data.head()
todelete = list()
counter = 0
print("[LOADED]\t processing...")
for i in list(data['Country']):
	if ((i != "France") and (i != "Portugal") and (i != "Sweden")):
		todelete.append(counter)
	counter +=1

print("[PROCESSED]\t deleting..")
data = data.drop(todelete, axis=0)
data.to_excel("../Online_retail.xlsx", index=False)
print("[FINISHED]")