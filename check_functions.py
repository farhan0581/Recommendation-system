from __future__ import division  # Python 2 users only
import os,re
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

x = 'extra'
print swn.senti_synsets(x,'n')[0]

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


dish = "chicken curry mughlai."
m = re.search(r'curr',dish)
if m:
	print m.group(0)
	print m.string
# print m.group(0)
