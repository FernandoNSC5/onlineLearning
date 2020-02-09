import sys
sys.path.append('../')
sys.path.append('../UTILS/')
import data_process

d = data_process.Data()

#Lista de antecedentes para o apriori rodar
antecedents = ['SET/20 RED RETROSPOT PAPER NAPKINS', 'SET/6 RED SPOTTY PAPER CUPS']

french = d.get_french_model()
french_antecedents = french['antecedents']
french_consequents = french['consequents']

#Printing model base
'''print("Model: ")
index = 0
print("Antecedent\t\tConsequent")
for i in french_antecedents:
	print(str(french_antecedents[index] + "\t" + str(french_consequents[index])))
	index += 1'''

n_c = list()
n_a = list()

#Converting frozen-set to list
for i in french_antecedents:
	n_a.append(list(i))
for i in french_consequents:
	n_c.append(list(i))

#Searching for results
index = 0
consequent = list()
for i in n_a:
	if not len(set(i).intersection(antecedents)):
		consequent.append(n_c[index]) 
	index += 1

#printing
for i in consequent:
	print(i)
		