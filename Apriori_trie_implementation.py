
import time
class trie_node:


	def __init__(self,value,parent=None):
		self.value = value
		self.parent=parent
		self.cover = []
		self.children = []

	def set_parent(self,parent):
		self.parent=parent

	def add_cover(self,transaction):
		self.cover.append(transaction)

	def add_child(self,node):
		self.children.append(node)


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

def solution(trie,numT,minFreq):
	"""Prints the solutions in correct format"""
	line=0
	for i in range(1,len(trie)): #for each level of the trie
		for node in trie[i]: #i loop over the nodes of the level
			if (len(node.cover)/numT >= minFreq): #if the node has a required frequency
				itemset=[node.value]
				parent=node.parent
				while ( parent.value != -1) : #rollback all the way to the root to get the full itemset
					itemset.append( parent.value )
					parent= parent.parent
				itemset.sort() # sort it to respect the order
				line+=1
				print(f"{itemset}  ({len(node.cover)/numT}) \n")
	print(line)



def check_answer(path_answer,path):
	"""Compare generated solution file with provided solution txt file"""
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

def apriori(filepath, minFrequency):
	"""Runs the apriori algorithm on the specified file with the given minimum frequency"""
	dat=Dataset(filepath)
	trie=[]
	trie.append([])
	origin=trie_node(-1)
	for item in dat.items:
		origin.add_child(trie_node(item,origin))
	for t in dat.transactions:
		origin.add_cover(t)
	trie[0].append(origin)
	for c in origin.children:
		for t in origin.cover:
			if c.value in t:
				c.add_cover(t)
	trie.append(origin.children)
	i=1

	while len(trie[i])>0: #we stop when the algorithm no longer generates new candidates
		#generate new candidates
		for j in range(len(trie[i])): # i take all leaves of F_i (previous level)
			k=j+1
			while (k<len(trie[i])) and ( (trie[i][j]).parent == (trie[i][k]).parent): # i check the right side neighbors
				new_leaf=trie_node( (trie[i][k]).value, trie[i][j]) # i create a leaf out of the right side neighbor
				# check support/cover
				for t in (new_leaf.parent).cover:  #i form the cover of this new leaf only out of the transactions that cover its parent
					if new_leaf.value in t:
						new_leaf.add_cover(t)
				# keep frequent itemsets
				trie.append([])

				if (len(new_leaf.cover)/dat.trans_num()) >= minFrequency: # if the new leaf forms a new frequent itemset i keep it
					trie[i+1].append(new_leaf) # by keeping it we mean linking it to the stored trie structure
					(new_leaf.parent).add_child(new_leaf) #and linking if to its parent
				k+=1
		i+=1
	solution(trie,dat.trans_num(),minFrequency) #printing the solutions out of the trie strucutre

	#check_answer("D://SINF2M//Q2//LINFO2364_Mining_Patterns//Template//result.txt","D://SINF2M//Q2//LINFO2364_Mining_Patterns//Datasets//toy_itemsets0125.txt")



t1=time.time()
apriori("D://SINF2M//Q2//LINFO2364_Mining_Patterns//Datasets//pumsb.dat",0.8)
t2=time.time()
print(t2-t1)