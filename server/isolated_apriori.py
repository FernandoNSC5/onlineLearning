import sys
sys.path.append('../')
sys.path.append('../UTILS/')
import data_process

d = data_process.Data()

#Lista de antecedentes para o apriori rodar
antecedents = ['SET/6 RED SPOTTY PAPER PLATES', 'SET/20 RED RETROSPOT PAPER NAPKINS']

french = d.get_french_model()
french_antecedents = french['antecedents']
french_consequents = french['consequents']

n_c = list()
n_a = list()

#Converting frozen-set to list
for i in french_antecedents:
	n_a.append(list(i))
for i in french_consequents:
	n_c.append(list(i))

#Printing model base
print("Model: ")
index = 0
print("Antecedent\t\tConsequent")
for i in n_a:
	print(str(n_a[index]) + "\t" + str(n_c[index]))
	index += 1

#Searching for results
index = 0
consequent = set()
print("\n\nPrinting Intersection of " + str(antecedents))
for i in n_a:
	if antecedents == i:
		consequent.add(str(n_c[index]))
	index+=1

'''index = 0
consequent = set()
print("\n\nPrinting Intersection of " + str(antecedents))
for i in n_a:
	print(str(set(i).intersection(antecedents)))
	if not len(set(i).intersection(antecedents)):
		consequent.add(str(n_c[index])) 
	index += 1
'''
#printing
print('\n\nResponse:')
for i in consequent:
	print(i)
		