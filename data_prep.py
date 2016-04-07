import csv
import os
import re

def get_dict():

	sentiment_dict = {}
	stopwords_list = []

	handle1 = open('data/adjective.txt','r')
	handle2 = open('data/noun.txt','r')
	handle3 = open('data/verb.txt','r')
	handle4 = open('data/adverb.txt','r')
	handle5 = open('data/int.txt','r')
	handle6 = open('data/new.txt','r')
	handle7 = open('data/stopwords.txt','r')

	# temp = handle5.read().splitlines()
	for line in handle5.readlines():
		d = line.split()
		x = d[0]
		x =  re.sub(r'_', " ", x)
		sentiment_dict[x] = d[1]

	for line in handle4.readlines():
		d = line.split()
		x = d[0]
		x =  re.sub(r'_', " ", x)
		sentiment_dict[x] = d[1]

	for line in handle3.readlines():
		d = line.split()
		x = d[0]
		x =  re.sub(r'_', " ", x)
		sentiment_dict[x] = d[1]

	for line in handle2.readlines():
		d = line.split()
		x = d[0]
		x =  re.sub(r'_', " ", x)
		sentiment_dict[x] = d[1]

	for line in handle1.readlines():
		d = line.split()
		x = d[0]
		x =  re.sub(r'_', " ", x)
		sentiment_dict[x] = d[1]

	for line in handle6.readlines():
		d = line.split()
		x = d[0]
		x =  re.sub(r'_', " ", x)
		sentiment_dict[x] = d[1]

	for line in handle7.readlines():
		d = line.split()
		x = d[0]
		stopwords_list.append(x)

	return sentiment_dict,stopwords_list

if __name__ == '__main__':
	x = get_dict()
	print x['love']