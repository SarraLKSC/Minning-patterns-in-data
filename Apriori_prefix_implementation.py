
import time


class Dataset:
	"""Utility class to manage a dataset stored in a external file."""

	def __init__(self, filepath):
		"""reads the dataset file and initializes files"""
		self.transactions = list()
		self.items = set()

		try:
			lines = [line.strip() for line in open(filepath, "r")]
			lines = [line for line in lines if line]  # Skipping blank lines
			for line in lines:
				transaction = list(map(int, line.split(" ")))
				self.transactions.append(transaction)
				for item in transaction:
					self.items.add(item)
		except IOError as e:
			print("Unable to read dataset file!\n" + e)

	def trans_num(self):
		"""Returns the number of transactions in the dataset"""
		return len(self.transactions)

	def items_num(self):
		"""Returns the number of different items in the dataset"""
		return len(self.items)

	def get_transaction(self, i):
		"""Returns the transaction at index i as an int array"""
		return self.transactions[i]



def Generate_candidates(F_i,level):
	C_i=[]
	i=0
	for i in range(len(F_i)): # for each item of the current frequent item set
		if(len(F_i[i])==level): #i take those of the current level of the search
			for j in range(i+1,len(F_i)): # i loop over the remaining frequent items
				if len(F_i[j])==level: # i take those of the current level of the search
					if F_i[i][:-1] == F_i[j][:-1]:
						if F_i[i][:-1] != []:
							new_item = F_i[i][:]
							new_item.append(F_i[j][-1])
						else:
							new_item=[F_i[i][-1]]
							new_item.append(F_i[j][-1])
						if new_item not in C_i:
							C_i.append(new_item)
	return C_i

def Determine_support(C_i,level,dat):
	D_i=[ 0 for _ in range(len(C_i))]

	for t in dat.transactions:
		if len(t)>=level:
			for i in range(len(C_i)):
				if all(x in t for x in C_i[i]):
					D_i[i]+=1
	return D_i

def check_answer(path_answer,path):

	f=open(path_answer,"r")
	original=open(path,"r")
	original_lines=original.readlines()
	answer_lines=f.readlines()
	ok=True
	if len(original_lines)== len(answer_lines):
		print(f"length {len(original_lines)}")
		for line in original_lines:
			if line not in answer_lines:
				ok=False
				break
	else:
		ok=False
	if ok:
		print("all good")
	else:
		print("not good")


def Frequent_itemsets(C_i,D_i,minFrequency,dat,freq):
	F=[]
	freq_=freq
	for i in range(len(C_i)):
		if ((D_i[i]/len(dat.transactions))>=minFrequency):
			F.append(C_i[i])
			freq_.append(D_i[i]/len(dat.transactions))
	return F,freq_


def apriori(filepath, minFrequency):
	"""Runs the apriori algorithm on the specified file with the given minimum frequency"""
	dat=Dataset(filepath)
	i=0
	stop=False
	solution =[]
	freq_sol=[]
	F_i=[ [item] for item in dat.items ]
	while (stop==False) :
		if(i>0):
			C_i=Generate_candidates(F_i,i)
			if len(C_i)==0:
				stop=True
		else:
			C_i=F_i
		D_i=Determine_support(C_i,i+1,dat)
		F_i,freq_sol=Frequent_itemsets(C_i,D_i,minFrequency,dat,freq_sol)
		[solution.append(f) for f in F_i]
		i+=1

	for i in range(len(solution)):
		print(f"{solution[i]}  ({freq_sol[i]})\n")






apriori("D://SINF2M//Q2//LINFO2364_Mining_Patterns//Datasets//mushroom.dat",0.6)
