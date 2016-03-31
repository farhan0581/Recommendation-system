import csv
import os
import re

def get_dict():

	sentiment_dict = {}

	handle1 = open('data/adjective.txt','r')
	handle2 = open('data/noun.txt','r')
	handle3 = open('data/verb.txt','r')
	handle4 = open('data/adverb.txt','r')
	handle5 = open('data/int.txt','r')

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

	return sentiment_dict