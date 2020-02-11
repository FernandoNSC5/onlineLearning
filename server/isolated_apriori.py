import data_process

HASHER = lambda x : hash(tuple(set(x)))

#Lista de antecedentes para o apriori rodar
antecedents = ['SET/6 RED SPOTTY PAPER PLATES', 'SET/20 RED RETROSPOT PAPER NAPKINS']
antecedents_h = HASHER(antecedents)

#Getting models
d = data_process.Data()
f = d.get_french_model()
f_a = f['antecedents']
f_c = f['consequents']

#Creating hash_list
n_a = list()
n_c = list() #this is not a hash -> consequent value store

#Processing model results
for i in f_a:
	n_a.append(HASHER(i))
for i in f_c:
	n_c.append(list(i))

#Generating subsequent array
r = list()
for i in range(len(n_a)):
	if n_a[i] == antecedents_h:
		r.append(n_c[i])

for i in r:
	print(i)