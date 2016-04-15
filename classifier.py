from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split,cross_val_score
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
import csv
import numpy as np
from numpy import array
from sklearn.externals import joblib


def get_classifier(docs_new):
	"""function which returns classifier"""

	handle=open('data/final_train.csv','r')
	reader=csv.DictReader(handle)

	#training data
	full_set=[]
	#response matrix
	response_full=[]

	for line in reader:
		full_set.append(line['review'])
		response_full.append(line['tag'])

	# # print c1,c2,c3
	# # print response_full
	response_full=array(response_full)
	# print response_full.shape


	# #building the vocabulary from the words of dishes
	count_vectorizer = CountVectorizer(stop_words='english')
	full_set_fit=count_vectorizer.fit_transform(full_set)

	# finding the term frequency
	# making idf false increases the accuracy in some cases
	tfidf_transformer = TfidfTransformer(use_idf=True)
	full_set_fit_tfidf = tfidf_transformer.fit_transform(full_set_fit)


	# splitting the dataset into train and test
	X_train, X_test, y_train, y_test=train_test_split(full_set_fit_tfidf,response_full,test_size=0.3)


	# training on the training dataset naeive baiyes
	clf = MultinomialNB().fit(X_train, y_train)

	# training using k neighbour
	knn=KNeighborsClassifier(n_neighbors=5)


	# k-fold testing on the dataset
	clf_kfold=MultinomialNB().fit(full_set_fit_tfidf, response_full)

	scores=cross_val_score(clf_kfold,full_set_fit_tfidf,response_full,cv=10,scoring='accuracy')
	print scores
	print 'mean score='+str(scores.mean()*100)


	# testing on some new dataset
	
	docs_new_s = count_vectorizer.transform(docs_new)
	docs_new_tfidf = tfidf_transformer.transform(docs_new_s)

	predicted = clf.predict(X_test)
	knn.fit(X_train,y_train)

	knn_predict=knn.predict(X_test)


	accuracy=metrics.accuracy_score(y_test,predicted)

	accuracy_knn=metrics.accuracy_score(y_test,knn_predict)

	print accuracy*100
	print accuracy_knn*100

	# clf_kfold = joblib.load('data/saved/clf_kfold.pkl')

	doc_pre=clf_kfold.predict(docs_new_tfidf)

	result = {}
	for i in range(len(docs_new)):
		# print doc_pre[i]
		# if doc_pre[i]==1:
		# 	print docs_new[i]+"--> Veg"
		# elif doc_pre[i]==0:
		# print docs_new[i] + '-->' + doc_pre[i]
		result[docs_new[i]] = doc_pre[i]

	return result

	# joblib.dump(clf_kfold, 'data/saved/clf_kfold.pkl') 

	# precision=metrics.precision_score(y_test, predicted)
	# recall=metrics.recall_score(y_test, predicted)
	# print recall
	# print precision


	# print "Vocabulary:", count_vectorizer.vocabulary_
	# count_vectorizer.get_feature.names()
	# freq_term_matrix = count_vectorizer.transform(train_set)
	# print freq_term_matrix.todense()

docs_new = ['The sitting which is mostly outdoor is the prettiest you can come across in CP',
			'Check out the pics to find out who greeted me on my first visit to Bercos CP branch, it can be expensive but not hygienic',
			'the restaurant declined to honour citibank offer of 15% off on the bill value with the reason that bill is generated',
			'ambiance','cocktails','dj system','menu','starter',
				'drinks','plate','costly','priced high','bill was burden on pocket','bill',
				'overpriced','OverPriced','resonable price','value for money']

print get_classifier(docs_new)