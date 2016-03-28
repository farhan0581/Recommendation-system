from __future__ import division  # Python 2 users only
import os,re
import time
# from nltk.book import *
# from nltk import udhr
from corenlp import StanfordCoreNLP
import nltk, re, pprint
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import pos_tag
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


# combine compound word
def compound_word(li):
	val = int(li['dependent'] - int(li['governor']))
	
	if abs(val) == 1:
		cword = li['dependentGloss'] + '-' + li['governorGloss']
		print cword

# checking for it and break on that basis
def check_for_it(sentence):
	sentence = sentence.replace('.It',',it')
	sentence = sentence.replace('. It',',it')
	sentence = sentence.replace('. it',',it')
	sentence = sentence.replace('.it',',it')
	return sentence
	

# splitting sentences on the basis of .?!
def split_sent(sentence):
	sentence = re.split('[.?!]',sentence)
	sentence = [x for x in sentence if x!='']
	return sentence 



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

def typedependencies(sent_list):

	pos_dict = {}
	depend_dict = {}
	depend_list = []
	
	nlp = StanfordCoreNLP('http://localhost:9000')
	for i in range(len(sent_list)):
		print sent_list[i]
		output = nlp.annotate(sent_list[i], properties={
    				'annotators': 'tokenize,ssplit,pos,depparse,parse,ner',
    				'outputFormat': 'json'
					})
		# pprint.pprint(output)
		x = output['sentences'][0]['basic-dependencies']
		# pprint.pprint(output['sentences'][0]['parse'])
		# pprint.pprint(x)
		print '-------------------------------------------------'
		for j in range(len(x)):
			
			if 'mod' in x[j]['dep'] or 'nsubj' in x[j]['dep']:
				print x[j]['dep'] + '-->' + x[j]['governorGloss'] + '-' + str(x[j]['governor']) + ' ' + x[j]['dependentGloss'] + '-' + str(x[j]['dependent'])
			if 'compound' in x[j]['dep']:
				compound_word(x[j])
			d = [x[j]['dep'],x[j]['governorGloss'],str(x[j]['governor']),x[j]['dependentGloss'],str(x[j]['dependent'])]
			depend_list.append(d)

		print ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
		for j in range(len(x)):
			# if 'mod' in x[j]['dep'] or 'nsubj' in x[j]['dep']:
			print x[j]['dep'] + '-->' + x[j]['governorGloss'] + '-' + str(x[j]['governor']) + ' ' + x[j]['dependentGloss'] + '-' + str(x[j]['dependent'])

		y = output['sentences'][0]['tokens']
		for k in range(len(y)):
			# if 'JJ' in y[k]['pos']:
			# 	print y[k]['lemma'] + ' --> ' + y[k]['pos']
			# 	try:
			# 		print swn.senti_synsets(y[k]['lemma'],'a')[0].pos_score()
			# 	except:
			# 		pass
			print y[k]['lemma'] + ' --> ' + y[k]['pos']
			pos_dict[y[k]['lemma']] = y[k]['pos']

		depend_dict[i] = depend_list
		depend_list = []

	print pos_dict
	print depend_dict


def preprocess(review):
	review = check_for_it(review)
	review = split_sent(review)
	return review


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

rev1= "Please go there for the ambience but also for the delicious food. The sitting which is mostly outdoor is the prettiest you can come across in CP. The drinks are a must have. The Giardino served in a lamp is beautiful and refreshing. The Nutty Jack is a delightful drink Bailey's, Jack Daniels served with peanut butter. Aam Papad Caprioska a perfect summer drink with chunks of aam papad. Starters: I absolutely recommend the Ganna Chicken a kebab wrapped on small sticks of sugar cane. Aam Aadmi Chicken yummy and spicy, this us served in a steel tiffin like old times. Chilli Paneer Ghosla is a nest of fried noodles stuffed with chilli panner topped with cheese slices. Red Gull Croquettes are cheese and potato croquettes served with a special redbull sauce. Main Course: the main course is filling and desi at heart. The Traphalgar Chicken Curry is perfectly spiced chicken curry. The biryani is on my must eat list. Desserts : the desserts are molecular gastronomy style. So we had a special UC Cake which is a cake and icing dipped in liquid nitrogen and topped with sauce. Molecular Lollies too are made with liquid nitrogen."
rev2 = 'We ordered a freiend of items from this place.I had ordered veg manchurian from here for an office meeting recently.Delicious veg manchurian.The service is quick, good value for money stuff.'
rev3 = 'This place has the best Chinese food especially their drumsticks are just so juicy and crunchy at the same time that I keep going to this place just to have a bite of them..'
rev4 = 'A good pocket friendly chinese or thai restaurant in CP. We ordered crispy chili potato and a combo of thai redcurry with rice. Chili potato was good and curry rice were awesome. We ordered DARSAN as a dessert, which was more like Indian version of jalebi with vanilla ice cream but it was good. Mint Mojito were also good. It will be great if they can make the place a bit more with lights which can make the place more ambient. Thanks Kapil'
rev5 = 'The tiger prawns here. It doesn\'t get better! One of the best places to have continental food. The ambience is luxurious! Loved the fried rice too, very generous portions. Noodles are a must try too. If you\'re in CP, do head here!'
rev6 = "When it comes to Chinese, Bercos and Yo china tops the list of any regular Chinese lover. These are the 2 mainstream famous restaurants serving delicious Chinese food, the Indian way. I absolutely love the Indo- Chinese version of Chinese food and not the Authentic Chinese served by biggies like Mainland China. I have been to the outlets of Bercos in Janakpuri District Centre and CP. I never experiment with Chinese food although i have tried a host of items like Vegetables in black bean sauce, Szechaun sauce. I never liked these items, nor the soups. It's not that they weren't properly done but i just go with very limited items. I always have Hakkah or Chilli Garlic noodles with Veg Gravy Munchurian for the mains. For the starters, Honey Chilli Potatoes and Spring rolls are the pre-decided orders. @DESIHABSHI has not tried a lot of different Chinese items but would like to recommend FA YIAN, a restaurant in the same lane, opposite to Bercos for an amazing experience. Till then, Enjoy at Bercos :D"
rev7 = "I was here with my friends for Dinner last Saturday. How to reach? If you commute by metro, get down at Rajeev Chowk and take the exit at Gate no 7 towards Baba Kharak Singh Marg. Take a right towards the outer block, walk 300m and there it is! For the starters we ordered the Chilli Garlic Crispy Vegetable and Vegetable Fried Wontons. I loved The Crispy Vegetables but found the Wontons to be devoid of any flavor. We also ordered their Signature Fruit Beer which tasted good! For the mains, I tried the Chilli Garlic Noodle accompanied with Assorted Vegetables in Garlic Sauce Followed by Garlic Steamed Rice and Vegetables in Black Pepper Sauce. All of these were delicious. The ambiance and interiors were soothing and welcoming. The staff was quick,courteous and even helped us with the chopsticks! Would I go back again? Yes, definitely!!"
rev8 = "We visited the TajMahal palace.Neither the food was good nor the serving."
rev9 = "Ardor is a really beautiful place with a giant terrace and lounge. A giant Restaurant and Lounge where you can party, dance and even spend a beautiful evening listening to some soul touching Sufi songs. Their fine dining restaurant is very well decorated and is Perfect for a dinner date. And their lounge is ideal for parties and for drinking and stuff. It's actually best of both worlds. Their food was pretty decent and the service was brilliant. The staff was very polite and humble towards the customers. I enjoyed my entire experience here :)"
rev0 = "The approach itself was so dirty, I wanted to go back but we had company & everyone was hungry. You cannot expect people to eat with a smelly, dirty ambience.The prices are high whereas the helpings are measly!!!!!!!!!!Taste, yes, I do not contest that. The food tastes good. But so does the Bengali food at Chittaranjan Park, at perhaps one third the price.Come on, wake up! if you expect people to come & eat & relish & recommend to friends & return, you need to take a look at how clean your place is or is not, how meagre your helpings are. After all, if we order Kosha Mangsho, I would expect some mutton, not bones with some flesh thrown in.This will not do."

nrev = 'Food was average and the restaurant declined to honour citibank offer of 15% off on the bill value with the reason that bill is generated. We unnecessary had to pay extra money just because of this reason and non cooperation of the staff.'
nrev1 = "Check out the pics to find out who greeted me on my first visit to Bercos CP branch. It can be expensive but not hygienic. I wonder how would be their kitchen. On top of it manager had guts to charge me too. I wish zomato introduce negative rating and big brands be more serious about food quality. Won't recommend."
nrev2 = "Total waste of money.\" Unhygienic toilets. Rude and cunning staff. Good Ambience. Chilli potato @starter priced Rs 500/- . They also added veg manchow soup of Rs 105/- in the bill which I didn't ordered. This is my 3rd experience with Bercos C.P., that every time they will add some extra thing in your bill. 2 times before I checked my bill but unfortunately not this time, so I paid extra amount. Total bill of Rs 1360/- + various taxes= 340/- Net amount = 1707/- And fun fact..... This happens @in happy hour."
nrev3 = "Had a horrible experience last Saturday (Feb 1, 2014) when I visited with some of my friends, as invited by a friend who had come to India from Singapore after a long time. We went upstairs where they have a bar, as my friends wanted to have drinks as well. Let me put it point-wise: 1. Service was like it doesn't exist, as all the waiters appear to be confused 2. It took 1.5 hours to serve crispy chilli potatoes!! 3. The place was too warm to sit there without getting suffocated 4. For my friends, most drinks that they had been mentioned on their drinks menu were not available! 5. It took one hour and repeated reminders to get a drink repeated for one of my friends 7. It took more than an hour to serve the dimsum platter 8. The waiters most of the time appeared clueless about what had been ordered from our table, they needed to be reminded again and again 9. The fried rice they served was not even boiled properly 10. When we asked for the bill, they gave us wrong bill, not just once, but twice!!!!! Now, where in the world this happens!! Thinking that they cant be wrong twice, we only realized after we had paid, on the second time!!! Third time they got it right. I think, there cant be a worse experience in a restaurant than this, at least it never had been like this for us. I was so embarrassed what memories my friend would take along to Singapore of Delhi and Bercos! Earlier we had some good memories of Bercos Noida, so we thought of trying it at CP as well. We even overlooked Irish bar and other much better places nearby, but Bercos CP proved us wrong. I suggest to all the readers that Bercos in CP is just waste of your time, CP has so many better places to eat, I'm sure. Food, service, ambiance, atmosphere, and cleanliness/hygiene, everything was a big let down. We even spoke to the manger later while leaving, but we could understand, he couldn't and wouldn't do much about it."
nrev4 = "I have been there once and was highly dissapointed~! When such restaurants serve cold Chinese food, there is nothing which upsets you more. The noodles were just about okay, warm but definitely not hot. The mixed vegetables in garlic sauce was average, nothing that you would want to come back for. The ambiance was great, we took some great pictures but nobody goes back for great ambiance!"



tokens = word_tokenize(review)
t = word_tokenize(rev2)


sent = preprocess(nrev3)
typedependencies(sent)


# text = ('I went to the Pita Pit restaurant yesterday.The food was delicious but serving was horrible there.')
# text = ('London is good at studies but bad at sports.')

    # print(output['sentences'][0]['parse'])
    # output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)
    # print(output)
    # output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
    # print(output)





# for w in t:
# 	if re.search('ts$',w):
# 		# print w
# 		print 'hi'

# porter = nltk.PorterStemmer()
# print [porter.stem(t) for t in tokens]

# print t
# fdist = nltk.FreqDist(t)
# for word in sorted(fdist):
# 	print('{}->{};'.format(word, fdist[word]))
	# pass
# parser = stanford.StanfordParser()

# pos = [nltk.pos_tag(word) for word in t]
# print type(pos)
# for word in t:
# print nltk.pos_tag(t)

# breakdown = swn.senti_synset('breakdown.n.03')
# print(breakdown)

# getting_namedentity(sent)











# stemmer = PorterStemmer()
# stemmer2 = SnowballStemmer("english")
# stemmer3 = WordNetLemmatizer()
# stemmer3.lemmatize("awesome")
# print stemmer3.lemmatize("prettiest")
# print stemmer.stem('prettiest')
# print stemmer2.stem('prettiest')
# print swn.senti_synsets('must','m')

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


