# Minning-patterns-in-data
The repo includes two versions of the apriori algorithm for minning patterns in transactional data.

* Frequent Itemset Mining (FIM) can be described as retriving the most frequent subsets of items from a set of given items based on a history of client transactions. 
A naive approach would consist in generated all possible combinations of items and tracking their counts through the transactional data. However in the era of big data this would
easily be proven unneficient as we face combinatorial explosion in the generation of the subsets and a far too cotsly time to count their appearences in the data.
One of many solutions to this task is the Apriori algorithm. The apriori algorithm is a baseline approach which relies on two fundamental concepts: 
anti-monotinicity and level-wise search. Anti-monotonicity states that is [A,B,C] is not frequent than undenaiably [A,B,C,D] is not either. Level-wise search follows the length
of the subsets strting from singleton.

* This repo regroups two versions of this algorithm the first one uses the prefix generation of new candidates (briefly if ABC and ABD  are frequent then i generate ABCD) 
the second version uses the trie structure which resembles the working of a tree.
