from __future__ import division  # Python 2 users only
import os,re,csv
import time
from data_prep import get_dict
# from nltk.book import *
# from nltk import udhr
from corenlp import StanfordCoreNLP
import nltk, re, pprint
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import pos_tag
import re
from nltk.corpus import stopwords
from nltk.corpus import reuters
from nltk.corpus import wordnet as wn
from nltk.parse import stanford
from nltk.corpus import sentiwordnet as swn
# from nltk.tag.stanford import NERTagger
from nltk.tag import StanfordNERTagger
from nltk.tag.hmm import HiddenMarkovModelTagger
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.parse.stanford import StanfordDependencyParser
from nltk.internals import find_jars_within_path
from operator import itemgetter
import itertools
import collections
import dpath.util

def split_sent(sentence):
    sentence = re.split('[.?!]',sentence)
    sentence = [x.lower() for x in sentence if x!='']
    return sentence 
# x = 'extra'
# print swn.senti_synsets(x,'n')[0]

# li = ['R','A']
# if li in 'A':
# 	print 'yes'
# print reuters.categories()
# li = stopwords.words('english')
# print len(li)
# for l in li:
# 	print l
li = ['1','2','farhan']
if 'farhan' in li:
	print 'k'

dishdic = {}

reader = csv.DictReader(open('data/trainfile.csv','r'))
for row in reader:
	if row['index'] == '3':
		dishdic[row['name']] = row['index']

# print len(dishdic)
# dish = "chicken curry mughlai."
# m = re.search(r'curr',dish)
# if m:
# 	# print m.group(0)
# 	# print m.string
# 	pass
print dishdic
# Ardor _reviews.csv
count = 0
ww = csv.writer(open('data/farhan2.csv','w'))
r = csv.DictReader(open('data/reviews/Dunkin\' Donuts _reviews.csv','r'))
for rr in r:
	sent = split_sent(rr['Review'])
	for key in dishdic.keys():
		for i in range(len(sent)):	
			if key in sent[i]:
				print sent[i]
				ww.writerow([sent[i].strip()])
				count = count + 1
				print '============================='

print count
# for (path, value) in dpath.util.search(dishdic, 'cost*', yielded=True):
# 	print path , value


# dic = {'1':'dasd','2':'asdf','3':'sdv'}
# dic = collections.OrderedDict(dic)
# x = dic._OrderedDict_map['2']
# for k,v in dic.items():
# 	print k.next
# j = 0
# for i in range(j,10):
# 	print i
# 	j = i + 2
# x = 0
# while x < 10:
# 	print x 
# 	x = x + 2