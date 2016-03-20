from __future__ import division  # Python 2 users only
import os,re
import time
# from nltk.book import *
# from nltk import udhr
import nltk, re, pprint
from nltk import word_tokenize,pos_tag,sent_tokenize
import re
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

java_path = "/usr/lib/jvm/java-8-oracle/jre/bin/java" # replace this
os.environ['JAVAHOME'] = java_path

os.environ['STANFORD_PARSER'] = '/home/farhan/Recommendation-system/stanford-ner-2015-12-09'
os.environ['STANFORD_MODELS'] = '/home/farhan/Recommendation-system/stanford-ner-2015-12-09/classifiers'


# getting the sentiment
def getting_sentiment(tagged):

	print '-------------------------------SENTIMENT----------------------------------'
	for i in range(0,len(tagged)):
		stemmer = WordNetLemmatizer()
		x = stemmer.lemmatize(tagged[i][0])
		if 'NN' in tagged[i][1] and len(swn.senti_synsets(x,'n')) > 0:
	    	# pscore+=(list(swn.senti_synsets(tagged[i][0],'n'))[0]).pos_score() #positive score of a word
	            # nscore+=(list(swn.senti_synsets(tagged[i][0],'n'))[0]).neg_score()  #negative score of a word
			print str(tagged[i][0]) + ' (noun)---> ' + str(swn.senti_synsets(x,'n')[0].pos_score())
		if 'JJ' in tagged[i][1] and len(swn.senti_synsets(x, 'a')) > 0:
			print str(tagged[i][0]) + ' (adjective)---> ' + str(swn.senti_synsets(x,'a')[0].pos_score())

		if 'VB' in tagged[i][0] and len(swn.senti_synsets(x,'v')) > 0:
			print str(tagged[i][0]) + ' (verb)---> ' + str(swn.senti_synsets(x,'v')[0].pos_score())

		if 'RB' in tagged[i][0] and len(swn.senti_synsets(x,'r')) > 0:
			print str(tagged[i][0]) + ' (adverb)---> ' + str(swn.senti_synsets(x,'r')[0].pos_score())

	print '-------------------------------SENTIMENT----------------------------------'



# getting the name entity
def getting_namedentity(sent):
	for i in range(len(sent)):
		tt = word_tokenize(sent[i])
		print '\n################ Tokenized version ###############'
		print tt
		tokenized = pos_tag(tt)
		print '\n################## Getting POS Tag ####################'
		print tokenized
		getting_sentiment(tokenized)
		# print tokenized
		namedent = nltk.ne_chunk(tokenized, binary=True)
		print '\n##################### Named Entity Recognition ###################'
		print namedent
		print '============================================================================================'



    # elif 'VB' in tagged[i][1] and len(swn.senti_synsets(tagged[i][0],'v'))>0:
    #        pscore+=(list(swn.senti_synsets(tagged[i][0],'v'))[0]).pos_score()
    #        nscore+=(list(swn.senti_synsets(tagged[i][0],'v'))[0]).neg_score()
    # elif 'JJ' in tagged[i][1] and len(swn.senti_synsets(tagged[i][0],'a'))>0:
    #        pscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).pos_score()
    #        nscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).neg_score()
    # elif 'RB' in tagged[i][1] and len(swn.senti_synsets(tagged[i][0],'r'))>0:
    #        pscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).pos_score()
    #        nscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).neg_score()

review = "Please go there for the ambience but also for the delicious food.\
The sitting which is mostly outdoor is the prettiest you can come across in CP.\
The drinks are a must have. The Giardino served in a lamp is beautiful and refreshing.\
The Nutty Jack is a delightful drink Bailey's, Jack Daniels served with peanut butter.\
Aam Papad Caprioska a perfect summer drink with chunks of aam papad. Starters: \
I absolutely recommend the Ganna Chicken a kebab wrapped on small sticks of sugar cane. \
Aam Aadmi Chicken yummy and spicy, this us served in a steel tiffin like old times.\
Chilli Paneer Ghosla is a nest of fried noodles stuffed with chilli panner topped with cheese slices. \
Red Gull Croquettes are cheese and potato croquettes served with a special redbull sauce. \
Main Course: the main course is filling and desi at heart. The Traphalgar Chicken Curry is perfectly spiced chicken curry.\
The biryani is on my must eat list. Desserts : the desserts are molecular gastronomy style.\
So we had a special UC Cake which is a cake and icing dipped in liquid nitrogen and topped with sauce.\
Molecular Lollies too are made with liquid nitrogen"

rev= "Please go there for the ambience but also for the delicious food. The sitting which is mostly outdoor is the prettiest you can come across in CP. The drinks are a must have. The Giardino served in a lamp is beautiful and refreshing. The Nutty Jack is a delightful drink Bailey's, Jack Daniels served with peanut butter. Aam Papad Caprioska a perfect summer drink with chunks of aam papad. Starters: I absolutely recommend the Ganna Chicken a kebab wrapped on small sticks of sugar cane. Aam Aadmi Chicken yummy and spicy, this us served in a steel tiffin like old times. Chilli Paneer Ghosla is a nest of fried noodles stuffed with chilli panner topped with cheese slices. Red Gull Croquettes are cheese and potato croquettes served with a special redbull sauce. Main Course: the main course is filling and desi at heart. The Traphalgar Chicken Curry is perfectly spiced chicken curry. The biryani is on my must eat list. Desserts : the desserts are molecular gastronomy style. So we had a special UC Cake which is a cake and icing dipped in liquid nitrogen and topped with sauce. Molecular Lollies too are made with liquid nitrogen."

tokens = word_tokenize(review)
t = word_tokenize(rev)


sent = sent_tokenize(rev)


###########################
# common python regex usage
###########################
# ^ exp matchfrom start
# $ exp match from end
# . wildcard
# + one or more of previous expressiom
# * zero or more of previous item

for w in t:
	if re.search('ts$',w):
		# print w
		print 'hi'

porter = nltk.PorterStemmer()
# print [porter.stem(t) for t in tokens]

# print t
fdist = nltk.FreqDist(t)
for word in sorted(fdist):
	print('{}->{};'.format(word, fdist[word]))
	# pass
# parser = stanford.StanfordParser()

# pos = [nltk.pos_tag(word) for word in t]
# print type(pos)
# for word in t:
# print nltk.pos_tag(t)

# breakdown = swn.senti_synset('breakdown.n.03')
# print(breakdown)

getting_namedentity(sent)


# 1. http://nlp.stanford.edu/software/stanford-corenlp-full-2015-04-20.zip
# 2 . Download version 3.6.0(english) and also version 3.5.2 ---> http://nlp.stanford.edu/software/lex-parser.shtml
# 3 . Download this -> http://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip
# ----------------------------------
# check if links are duplicate












# stemmer = PorterStemmer()
# stemmer2 = SnowballStemmer("english")
# stemmer3 = WordNetLemmatizer()
# stemmer3.lemmatize("awesome")
# print stemmer3.lemmatize("prettiest")
# print stemmer.stem('prettiest')
# print stemmer2.stem('prettiest')
# print swn.senti_synsets('must','m')
# print swn.senti_synsets('pretty','a')[0].pos_score()

# sent = "My name is Farhan Khan and I live in New Delhi"


# print HiddenMarkovModelTagger(tokenized)
# t = pos_tag(t)

# se = 'I went to the Young Blues restaurant,The food was awesome there.'
# se = word_tokenize(se)
# se = pos_tag(se)
# english_nertagger = StanfordNERTagger("/home/farhan/Recommendation-system/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz",
	# "/home/farhan/Recommendation-system/stanford-ner-2015-12-09/stanford-ner.jar")
# li = english_nertagger.tag('Rami Eid is studying at Stony Brook University in NY'.split())



# nltk.download()
# base_path = os.path.dirname(os.path.dirname(__file__))
# path = os.path.join(base_path, "Recommendation-system","static")
# print base_path
# time.sleep(5)
# print path
# if not os.path.exists(path):
# 	os.makedirs(path,0777)
# languages = ['Chickasaw', 'English', 'German_Deutsch',
#     'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
# cfd = nltk.ConditionalFreqDist(
#           (lang, len(word))
#           for lang in languages
#          for word in udhr.words(lang + '-Latin1'))
# cfd.plot(cumulative=True)

# dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
# stanford_dir = st._stanford_jar.rpartition('/')[0]
# # or in windows comment the line above and uncomment the one below:
# #stanford_dir = st._stanford_jar.rpartition("\\")[0]
# stanford_jars = find_jars_within_path(stanford_dir)
# st.stanford_jar = ':'.join(stanford_jars)
# [parse.tree() for parse in dep_parser.raw_parse("The quick brown fox jumps over the lazy dog.")]


