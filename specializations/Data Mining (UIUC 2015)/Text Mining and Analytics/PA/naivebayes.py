import math

def BayesianScore(train_docs, train_labels, nvocab, test_docs, test_label1, test_label2):
	ndocs = len(train_docs) # = len(train_labels)
	allwords, alllabels = [], list(set(train_labels))
	P = {}
	for i in range(ndocs):
		doc, label = train_docs[i], train_labels[i]
		P[label] = P.get(label, 0.0) + 1.0 	# Prior
		words = doc.lower().split()
		allwords += words
		for word in words:
			P[(word, label)] = P.get((word, label), 0.0) + 1.0
	for label in alllabels:
		P[label] /= ndocs
	allwords = set(allwords)
	Z = {label: sum([P.get((word, label), 0.0) for word in allwords]) + nvocab for label in alllabels}
	for word in allwords:
		for label in alllabels:
			P[(word, label)] = (P.get((word, label), 0.0) + 1.0) / Z[label]
	print P
	for doc in test_docs:
		words = doc.lower().split()
		print doc, math.log(P[test_label1] / P[test_label2]) + sum([math.log(P.get((word, test_label1), 0.0) / P.get((word, test_label2), 0.0)) for word in words])
		P_doc_test_label1, P_doc_test_label2 = 1.0, 1.0
		for word in words:
			P_doc_test_label1, P_doc_test_label2 = P_doc_test_label1 * P.get((word, test_label1), 0.0), P_doc_test_label2 * P.get((word, test_label2), 0.0)
		prob = 1.0 / (1.0 + (P_doc_test_label2 * P[test_label2]) / (P_doc_test_label1 * P[test_label1]))
		print 'Prob', test_label1, doc, prob
		#print math.log(prob / (1 - prob)), math.log(P_doc_test_label1 * P[test_label1] / (P_doc_test_label2 * P[test_label2]))
		#print (P_doc_test_label2 * P[test_label2]) / (P_doc_test_label1 * P[test_label1]), P_doc_test_label2 / P_doc_test_label1, P_doc_test_label1, P_doc_test_label2
		
train_docs = ['Save Money No Fees', 'Back to the Future', 'Back to School Night']
train_labels = ['Spam', 'Ham', 'Ham']
nvocab = 10
test_docs = ['No fees', 'Save money back', 'Save money future', 'Future school no fees']

BayesianScore(train_docs, train_labels, nvocab, test_docs, 'Spam', 'Ham')