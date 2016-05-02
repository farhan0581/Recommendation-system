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
import dpath.util

def get_dish_lookup():
	result = {}
	handle = open('data/zomato_dishes.csv','r')
	reader = csv.DictReader(handle)
	for row in reader:
		result[row['dish']] = 1
	return result

def get_lookup_dict():

	result = {}
	handle = open('data/trainfile.csv','r')
	reader = csv.DictReader(handle)
	for row in reader:
		if row['index'] == '0':
			tag = 'general'
		elif row['index'] == '1':
			tag = 'food'
		elif row['index'] == '2':
			tag = 'ambience'
		elif row['index'] == '3':
			tag = 'cost'
		elif row['index'] == '4':
			tag = 'service'

		result[row['name']] = tag
	return result



def check_in_dic(string):
	"""function which performs search on 
		the dish dictionary"""
	handle = open('data/zomato_dishes.csv','r')
	reader = csv.DictReader(handle)
	dish = {}
	for row in reader:
		dish[row['dish'].lower()] = row['index']

	search_string = string.lower()
	for (path, value) in dpath.util.search(dish, search_string, yielded=True):
		return path




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

	doc_pre=clf_kfold.predict(docs_new_tfidf)
	# print docs_new_tfidf.shape
	# print full_set_fit_tfidf.shape
	# (10, 6689)
	# (9693, 6689)
	result = {}
	for i in range(len(docs_new)):
		result[docs_new[i]] = doc_pre[i]

	joblib.dump(clf_kfold, 'data/saved/clf_kfold.pkl') 
	joblib.dump(count_vectorizer.vocabulary_,'data/saved/dict.pkl')

	return result

def get_trained_classifier(docs_new,original):

	# need to save the classifier as well as the size dictionary
	# to avoid any size mismatch error
	clf_kfold = joblib.load('data/saved/clf_kfold.pkl')
	dic = joblib.load('data/saved/dict.pkl')

	count_vectorizer = CountVectorizer(stop_words='english',vocabulary=dic)
	full_set_fit=count_vectorizer.fit_transform(docs_new)

	tfidf_transformer = TfidfTransformer(use_idf=True)
	full_set_fit_tfidf = tfidf_transformer.fit_transform(full_set_fit)

	doc_pre=clf_kfold.predict(full_set_fit_tfidf)

	result = {}
	for i in range(len(docs_new)):
		x = original[docs_new[i]]
		x.append(doc_pre[i])
		result[docs_new[i]] = x

	return result



	# precision=metrics.precision_score(y_test, predicted)
	# recall=metrics.recall_score(y_test, predicted)
	# print recall
	# print precision


	# print "Vocabulary:", count_vectorizer.vocabulary_
	# count_vectorizer.get_feature.names()
	# freq_term_matrix = count_vectorizer.transform(train_set)
	# print freq_term_matrix.todense()









docs_new = ['drinks','plate','costly','priced high','bill was burden on pocket','bill',
				'overpriced','OverPriced','resonable price','value for money']

# print get_classifier(docs_new)
# print get_trained_classifier(docs_new)
# print get_lookup_dict()

# print check_in_dic('')
