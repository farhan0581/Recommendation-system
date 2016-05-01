from __future__ import division  # Python 2 users only
import os
import re
import time
from data_prep import get_dict
# from nltk.book import *
# from nltk import udhr
from corenlp import StanfordCoreNLP
import nltk
import pprint
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
from operator import itemgetter
import itertools
import collections
import dpath.util
from classifier import get_lookup_dict,get_trained_classifier,check_in_dic
from final_scores import final_scores


java_path = "/usr/lib/jvm/java-8-oracle/jre/bin/java"  # replace this
os.environ['JAVAHOME'] = java_path

os.environ['STANFORD_PARSER'] = '/home/farhan/Recommendation-system/stanford-ner-2015-12-09'
os.environ['STANFORD_MODELS'] = '/home/farhan/Recommendation-system/stanford-ner-2015-12-09/classifiers'

# defining global parameters
score_dic,stopwords = get_dict()
neg_prefix = ['not','none','nor','n\'t']
# final_score = {}
# compound_word_dic = {}
# compound_word_list = []
# neg_words = []


# checking for any dish present...


# combine compound word
def compound_word(li):
    # print li
    word = []
    st = ''
    length = len(li)
    i = 0
    while i < length:
        while True:
            a = li[i][0]
            try:
                b = li[i+1][0]
            except IndexError:
                i = i + 1
                if st not in word:
                    word.append(st.strip())
                break
            if b-a == 1:
                if li[i][1].lower() not in st:
                    st = st + ' ' + li[i][1].lower() + ' ' + li[i+1][1].lower() + ' '
                else:
                    st = st + ' ' + li[i+1][1].lower() + ' '
                i = i + 1
            else:
                word.append(st.strip())
                i = i + 1
                st = ''
                break
    return word


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
def getting_sentiment(word,pos):
    flag = 0
    if 'NN' in pos:
        tag = 'n'
    elif 'JJ' in pos:
        tag = 'a'
        if pos == 'JJS':
            flag = 1
    elif 'VB' in pos:
        tag = 'v'
    elif 'RB' in pos:
        tag = 'r'
    else:
        tag = ''
    stemmer = WordNetLemmatizer()
    if tag != '':
        x = stemmer.lemmatize(word,tag)
    else:
        x = stemmer.lemmatize(word)

    try:
        score = float(score_dic[x]) #* float(m1)
    except KeyError:
        if len(swn.senti_synsets(x,tag)) > 0:
            score = swn.senti_synsets(x,tag)[0].pos_score() * 5
        else:
            score = 100

    if flag == 1 and score != -100 and score < 4:
        score = score + 1
    elif flag == 1 and score != -100 and score > -4 and score < 0:
        score = score - 1
    print word + '--->' + str(score)
    return score






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
        print '\n##################### Named Entity Recognition #############'
        print namedent
        print '========================================================'

# getting typed dependencies using stanford parser
def typedependencies(sent_list,neg_words,compound_word_list):

    pos_dict = {}
    depend_dict = {}
    depend_list = []
    proper_names = []
    # neg_words = []
    compound_dic = {}
    
    nlp = StanfordCoreNLP('http://localhost:9000')
    for i in range(len(sent_list)):
        compound_list = []
        print sent_list[i]
        output = nlp.annotate(sent_list[i], properties={
                    'annotators': 'tokenize,ssplit,pos,depparse,parse,ner',
                    'outputFormat': 'json'
                    })
        # pprint.pprint(output)
        x = output['sentences'][0]['basic-dependencies']
        # pprint.pprint(output['sentences'][0]['parse'])
        # pprint.pprint(x)
        # print '-------------------------------------------------'
        for j in range(len(x)):
         
            if 'compound' in x[j]['dep']:
                # compound_word(x[j])
                ll = [x[j]['governorGloss'],x[j]['governor'],
                        x[j]['dependentGloss'],x[j]['dependent']]
                compound_dic[x[j]['governor']] = x[j]['governorGloss']
                compound_dic[x[j]['dependent']] = x[j]['dependentGloss']
                # compound_list.append(ll)

            d = [x[j]['dep'],x[j]['governorGloss'],str(x[j]['governor'])
                ,x[j]['dependentGloss'],str(x[j]['dependent'])]
            depend_list.append(d)


            # getting the negative words..
            if 'neg' in x[j]['dep']:
                x1 = x[j]['governorGloss'].lower()
                x2 = x[j]['dependentGloss'].lower()
                if x1 not in stopwords:
                    neg_words.append(x1)
                else:
                    neg_words.append(x2)

            if 'conj' in x[j]['dep']:
                x1 = x[j]['governorGloss'].lower()
                x2 = x[j]['dependentGloss'].lower()
                if x1 in neg_prefix:
                    neg_words.append(x2)
                # elif (x2 == 'not' or x2 == 'nor' or x2 == 'non'):
                #   neg_words.append(x1)
                elif x2 in neg_prefix:
                    neg_words.append(x1)

            print (x[j]['dep'] + '-->' + x[j]['governorGloss'] + '-' 
                + str(x[j]['governor']) + ' ' + x[j]['dependentGloss'] +
                 '-' + str(x[j]['dependent']))
        print '==================================='
        

        for key,value in sorted(compound_dic.items()):
            compound_list.append([key,value])
        # print compound_word(compound_list)  
        compound_dic.clear()
        

        y = output['sentences'][0]['tokens']
        for k in range(len(y)):
            pos_dict[y[k]['word']] = y[k]['pos']
            if 'NNP' in y[k]['pos']:
                proper_names.append(y[k]['word'])

        depend_dict[i] = depend_list
        depend_list = []

        if len(compound_list) > 0:
            w = compound_word(compound_list)
        else:
            w = []
        for jj in range(len(w)):
            if w[jj] != '':
                print w[jj]
                compound_word_list.append(w[jj])

    print '--------NAMES------' + str(proper_names)
    print '--------NEGATIVE----' + str(neg_words)
    return depend_dict,pos_dict,proper_names

def apply_score(li,n,score,final_score,meaning,m,t1,t2):
    # print li,n,score,final_score,meaning,m,t1,t2
    try:
        x = final_score[n]
        if ((abs(int(x[1])-int(x[2])) < abs(int(li[2])-int(li[4])))
            ):
            if meaning > x[3]:
                final_score[n] = [score,li[2],li[4],meaning,m]
            else:
                final_score[n] = x

        elif abs(int(x[1])-int(x[2])) == abs(int(li[2])-int(li[4])):
        
            if float(x[0]) >= float(score) and x[3] >= meaning:
                final_score[n] = x
            else:   
                final_score[n] = [score,li[2],li[4],meaning,m]

        elif abs(int(x[1])-int(x[2])) > abs(int(li[2])-int(li[4])):
            print '===here'
            if x[3] <= meaning:
                final_score[n] = [score,li[2],li[4],meaning,m]
            else:
                final_score[n] = x
        else:
            final_score[n] = [score,li[2],li[4],meaning,m]

    except KeyError:
        final_score[n] = [score,li[2],li[4],meaning,m]

    # return final_score


def check_for_negative(a,b,neg_words):

    x = y = 1
    for i in range(len(neg_words)):
        if a in neg_words[i]:
            x = -1
        elif b in neg_words[i]:
            y = -1
    return x,y

def check_for_single_negative(word,neg_words):
    x = 1
    for i in range(len(neg_words)):
        if word in neg_words[i]:
            x = -1
    return x


# function to parse and check the significance of root word
def check_for_root(dlist,poslist,final_score,neg_words):
    # print dlist
    # print poslist
    # print final_score
    # print '============='

    for key,value in dlist.items():
        lis1 = []
        lis2 = []
        li = {}
        lis = value
        for i in range(len(lis)):
            if i == 0:
                if 'ROOT' in lis[0]:
                    root = lis[0][3]
                    rootp = lis[0][4]
            else:
                if root in lis[i]:
                    if lis[i][1] == root and lis[i][2] == rootp:
                        lis1.append([lis[i][3],lis[i][4]])
                    elif lis[i][3] == root and lis[i][4] == rootp:
                        lis1.append([lis[i][1],lis[i][2]])
        # making lis2
        for i in range(len(lis1)):
            for j in range(1,len(lis)):
                if lis1[i][0] in lis[j]:
                   
                    if lis[j][1] == lis1[i][0] and lis[j][1] != root:
                        lis2.append([lis[j][3],lis[j][4]])
                    elif lis[j][3] == lis1[i][0] and lis[j][1] != root:
                        lis2.append([lis[j][1],lis[j][2]])
         
        pos_root = poslist[root]
        # now check if root is significant
        if (root.lower() not in stopwords and 'NN' in pos_root or 'JJ' in
            pos_root ):
           
            rootscore = getting_sentiment(root.lower(),pos_root)
            m = check_for_single_negative(root,neg_words)
            rootscore = rootscore * m
            if (rootscore != 100) :
                for i in range(len(lis2)):
                    if lis2[i][0].lower() not in stopwords:
                        wordpos = poslist[lis2[i][0]]
                        if ('JJ' in wordpos or 'NN' in wordpos and 
                            wordpos != pos_root):
                            if (check_ifnotpresentin_scores(lis2[i][0],root,
                                    lis2[i][1],rootp,rootscore,final_score) == 1):
                                final_score[lis2[i][0].lower()] = [rootscore,lis2[i][1],rootp,1,root] 
                                # print root,lis2[i][0],rootp,lis2[i][1]
            else:
                for i in range(len(lis2)):
                    if lis2[i][0].lower() not in stopwords:
                        wordpos = poslist[lis2[i][0]]
                        if ('JJ' in wordpos or 'NN' in wordpos and wordpos 
                            != pos_root):
                            score = getting_sentiment(lis2[i][0].lower(),wordpos)
                            if score != 100:
                                m2 = check_for_single_negative(lis2[i][0],neg_words)
                                score = score * m2
                                if (check_ifnotpresentin_scores(lis2[i][0],root,
                                    lis2[i][1],rootp,score,final_score) == 1):
                                    final_score[root.lower()] = [score,rootp,lis2[i][1],1,lis2[i][0]] 
                                    # print lis2[i][0],root
                                    # print ':::::::::::'

        else:
            # print 'root is a stopword'
            pass

    # print lis1
    # print lis2


def check_ifnotpresentin_scores(word1,word2,ps1,ps2,score,final_score):
    
    flag = 0
    try:
        x = final_score[word1]
        if (x[4] == word2 and x[1] == str(ps1) and 
            x[2] == str(ps2) ):
            flag = 0
            # print 'ALREADY PRESENT-----------'
        else:
            if x[3] == 2 or x[0] > score:
                flag = 0
                # print 'low score=-----------'
            else:
                flag = 1
                # print 'high score-------------'

    except KeyError:
        flag = 1
        # print 'not present--------------------'
    return flag


def check_for_noun_adj(depend_dict, pos_dict,final_score,neg_words):

    # getting the score and stopwords dictionary
    sd,stopwords = get_dict()
    flag = 0
    stemmer3 = WordNetLemmatizer()
    for value in depend_dict.values():
        
        for j in range(len(value)):
            score1 = 100
            score2 = 100
            li = value[j]
            if "nsubj" in li[0] or "mod" in li[0]:
                meaning = 0.2
                n1 = li[1]
                n2 = li[3]
                m1, m2 = check_for_negative(n1,n2,neg_words)
                try:
                    t1 = pos_dict[n1]
                except KeyError:
                    # print n1 + ' is not there!!'
                    flag = 1
                try:
                    t2 = pos_dict[n2]
                except KeyError:
                    # print n2 + ' is not there!!'
                    flag = 1
                if (flag != 1 and n1.lower() not in stopwords
                     and n2.lower() not in stopwords):
            
                    score1 = getting_sentiment(n1.lower(),t1)
                    if score1 != 100:
                        score1 = float(score1) * float(m1)
                    score2 = getting_sentiment(n2.lower(),t2)
                    if score2 != 100:
                        score2 = float(score2) * float(m2)

                    if score1 != 100 or score2 != 100:
                        if 'NN' in t1 or 'NN' in t2:
                            if 'JJ' in t1 or 'JJ' in t2:
                                meaning = 1
                                # print n1 + ' and ' + n2 + ' appear to be  meaningful...'
                            elif ('VB' in t1 or 'VB' in t2
                                or ('NN' in t1 and 'NN' in t2)):
                                # print n1 + ' and ' + n2 + ' appear to be less meaningful...'
                                meaning = 0.8
                        else:                         
                            meaning = 0.2
                        if score1 != 100 and score2 == 100:
                            apply_score(li,n2,score1,final_score,meaning,n1,t2,t1)
                            print n1,n2
                        if score2 != 100 and score1 == 100:
                            print n2,n1
                            apply_score(li,n1,score2,final_score,meaning,n2,t1,t2)

                        elif score2 != 100 and score1 != 100:
                            if 'NN' in t1 and 'JJ' in t2:
                                # print n1,n2
                                apply_score(li,n1,score2,final_score,meaning,n2,t1,t2)
                            elif 'JJ' in t1 and 'NN' in t2:
                                apply_score(li,n2,score1,final_score,meaning,n1,t2,t1)
                                # print n1,n2
                            elif 'NN' in t1:
                                apply_score(li,n1,score2,final_score,meaning,n2,t1,t2)
                                # print n1,n2
                            elif 'NN' in t2:
                                apply_score(li,n2,score1,final_score,meaning,n1,t2,t1)
                                # print n1,n2

                    else:
                        # print 'The scores are not present for ' + n1 + ' and ' + n2
                        pass

            # checking for direct object or dependency...
            if 'dobj' in li[0] or 'dep' in li[0]:
                n1 = li[1]
                n2 = li[3]
                m1, m2 = check_for_negative(n1,n2,neg_words)
                t1 = pos_dict[n1]
                t2 = pos_dict[n2]
                score1 = 100
                score2 = 100
                score1 = getting_sentiment(n1.lower(),t1)
                if score1 != 100:
                    score1 = float(score1) * float(m1)
                score2 = getting_sentiment(n2.lower(),t2)
                if score2 != 100:
                    score2 = float(score2) * float(m2)

                if score1 != 100 or score2 != 100:
                    if (n1.lower() not in stopwords and
                         n2.lower() not in stopwords):
                        if 'NN' in t1 or 'NN' in t2:
                            if 'JJ' in t1 or 'JJ' in t2:
                                meaning = 1
                                # print n1,t1 + ' and ' + n2,t2 + ' adjective-noun as direct object...'
                            else:
                                if ('VB' in t1 or 'VB' in t2 or 
                                    ('NN' in t1 and 'NN' in t2)):
                                    meaning = 0.8
                                # print n1,t1 + ' and ' + n2,t2 + ' as direct object...'
                        else:
                            meaning = 0.2
                            # print 'no noun occurance'


                        if score2 != 100 and score1 == 100:
                            apply_score(li,n1,score2,final_score,meaning,n2,t1,t2)
                        elif score1 != 100 and score2 == 100:
                            apply_score(li,n2,score1,final_score,meaning,n1,t2,t1)
                        elif score1 != 100 and score2 != 100:
                            if 'NN' in t1 and 'JJ' in t2:
                                apply_score(li,n1,score2,final_score,meaning,n2,t1,t2)
                            elif 'JJ' in t1 and 'NN' in t2:
                                apply_score(li,n2,score1,final_score,meaning,n1,t2,t1)
                            elif score1 > score2:
                                apply_score(li,n2,score1,final_score,meaning,n1,t2,t1)
                            elif score2 >= score1:
                                apply_score(li,n1,score2,final_score,meaning,n2,t1,t2)


                    else:
                        print '-----------stopwords-----------'

            # check if compound word present



def preprocess(review):
    review = check_for_it(review)
    review = split_sent(review)
    return review


def replace_with_compoundword(score,dic):
    # print score
    # print dic

    for key in score.keys():
        for k in dic.keys():
            if key.lower() in k.lower():
                try:
                    x = score[key]
                    del score[key]
                    score[k] = x
                except KeyError:
                    pass
    # print score


def cross_validate():
    """cross validating the scores dictionary"""
    pass

                    # print '/////////////////////////  


    # elif 'VB' in tagged[i][1] and len(swn.senti_synsets(tagged[i][0],'v'))>0:
    #        pscore+=(list(swn.senti_synsets(tagged[i][0],'v'))[0]).pos_score()
    #        nscore+=(list(swn.senti_synsets(tagged[i][0],'v'))[0]).neg_score()
    # elif 'JJ' in tagged[i][1] and len(swn.senti_synsets(tagged[i][0],'a'))>0:
    #        pscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).pos_score()
    #        nscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).neg_score()
    # elif 'RB' in tagged[i][1] and len(swn.senti_synsets(tagged[i][0],'r'))>0:
    #        pscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).pos_score()
    #        nscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).neg_score()

revi = "Please go there for the ambience but also for the delicious food.\
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
rev8 = "We visited the PitaPit restaurant.Neither the food was good nor the serving."
rev9 = "Ardor is a really beautiful place with a giant terrace and lounge. A giant Restaurant and Lounge where you can party, dance and even spend a beautiful evening listening to some soul touching Sufi songs. Their fine dining restaurant is very well decorated and is Perfect for a dinner date. And their lounge is ideal for parties and for drinking and stuff. It's actually best of both worlds. Their food was pretty decent and the service was brilliant. The staff was very polite and humble towards the customers. I enjoyed my entire experience here :)"
rev0 = "The approach itself was so dirty, I wanted to go back but we had company & everyone was hungry. You cannot expect people to eat with a smelly, dirty ambience.The prices are high whereas the helpings are measly!!!!!!!!!!Taste, yes, I do not contest that. The food tastes good. But so does the Bengali food at Chittaranjan Park, at perhaps one third the price.Come on, wake up! if you expect people to come & eat & relish & recommend to friends & return, you need to take a look at how clean your place is or is not, how meagre your helpings are. After all, if we order Kosha Mangsho, I would expect some mutton, not bones with some flesh thrown in.This will not do."
rev11 = "Odeon social is the new addition to the social legacy. From ambience to food to service to the entrance as well ,everything was just mind blowing. The servers wearing school uniform and the mark sheet board definitely takes you back to ur school days. The service was fast and efficient. Ordered: a glass of Sula satori Merlot Malbec ,cheese Masala pao,chilly paneer black pepper box,shawarma wrap,yo mama. Chilly paneer black pepper box was excellent. The sauce was perfectly made. Shawarma wrap was delicious. Garlic mayo and fries were the stars. The masala used on the fries reminded me of fries from McDonald's. Cheese masala pao!!lip smacking is the correct word. Loved it to last bite. I was full but still couldn't resist myself from finishing he dish. Overall it's an amazing new place in cp and a must try."

nrev = 'Food was average and the restaurant declined to honour citibank offer of 15% off on the bill value with the reason that bill is generated. We unnecessary had to pay extra money just because of this reason and non cooperation of the staff.'
nrev1 = "Check out the pics to find out who greeted me on my first visit to Bercos CP branch. It can be expensive but not hygienic. I wonder how would be their kitchen. On top of it manager had guts to charge me too. I wish zomato introduce negative rating and big brands be more serious about food quality. Won't recommend."
nrev2 = "Total waste of money.\" Unhygienic toilets. Rude and cunning staff. Good Ambience. Chilli potato @starter priced Rs 500/- . They also added veg manchow soup of Rs 105/- in the bill which I didn't ordered. This is my 3rd experience with Bercos C.P., that every time they will add some extra thing in your bill. 2 times before I checked my bill but unfortunately not this time, so I paid extra amount. Total bill of Rs 1360/- + various taxes= 340/- Net amount = 1707/- And fun fact..... This happens @in happy hour."
nrev3 = "Had a horrible experience last Saturday (Feb 1, 2014) when I visited with some of my friends, as invited by a friend who had come to India from Singapore after a long time. We went upstairs where they have a bar, as my friends wanted to have drinks as well. Let me put it point-wise: 1. Service was like it doesn't exist, as all the waiters appear to be confused 2. It took 1.5 hours to serve crispy chilli potatoes!! 3. The place was too warm to sit there without getting suffocated 4. For my friends, most drinks that they had been mentioned on their drinks menu were not available! 5. It took one hour and repeated reminders to get a drink repeated for one of my friends 7. It took more than an hour to serve the dimsum platter 8. The waiters most of the time appeared clueless about what had been ordered from our table, they needed to be reminded again and again 9. The fried rice they served was not even boiled properly 10. When we asked for the bill, they gave us wrong bill, not just once, but twice!!!!! Now, where in the world this happens!! Thinking that they cant be wrong twice, we only realized after we had paid, on the second time!!! Third time they got it right. I think, there cant be a worse experience in a restaurant than this, at least it never had been like this for us. I was so embarrassed what memories my friend would take along to Singapore of Delhi and Bercos! Earlier we had some good memories of Bercos Noida, so we thought of trying it at CP as well. We even overlooked Irish bar and other much better places nearby, but Bercos CP proved us wrong. I suggest to all the readers that Bercos in CP is just waste of your time, CP has so many better places to eat, I'm sure. Food, service, ambiance, atmosphere, and cleanliness/hygiene, everything was a big let down. We even spoke to the manger later while leaving, but we could understand, he couldn't and wouldn't do much about it."
nrev4 = "I have been there once and was highly dissapointed~! When such restaurants serve cold Chinese food, there is nothing which upsets you more. The noodles were just about okay, warm but definitely not hot. The mixed vegetables in garlic sauce was average, nothing that you would want to come back for. The ambiance was great, we took some great pictures but nobody goes back for great ambiance!"
nrev5 = "Please carry id proof with you if you want to have cocktails . worst restaurant ever visit in cp and there service is very slow as compare to other restaurants"
sample = "The food was very good but the ambience was pathetic"
nrev6 = "Very unapologetic staff.. I went there on 3rd April got a big METAL piece in my chicken dish. The staff there were behaving as if I have put that metal piece in my dish.. Moreover staff included that dish in my bill. Till that instance it used to be my favourite place for Chinese food.. But now I don't think I can again go there and have that piece of metal, and facing that rude staff"
nrev7 = "This place has turned into SHIT recently. No wonder nobody comes there even on weekends. I went there along with my family and friends on Sunday. I was surprised to see there were no customers. We went inside. It took them 10 minutes to bring the menu.We ordered something on which they asked for the Photo ID on which I produced it to them. Later on they started demanding the ID for everyone. Such a redeculious behaviour. The waiter kept arguing on which we requested him to call the manager. Manager came and repeated his lines like a parrot without logic. 3 out of 5 of us showed him our IDs. Its not necessary for everyone to carry an ID. They kept on arguing for each members ID and refused to serve. Such a insult to a customer. We left the place without having anything. PLEASE DON'T VISIT IT. - Yes, this is coming from a frequent visitor of this place. I have been here about more than 50 times and liked this place. BUT it has turned into horrible place with lack of customer service. Looks like they are no more interested in Restaurant Business. AVOID BERCOS CP Outlet."
nrev8 = "I'm a big fan of the hauz khas social. So I definitely wanted to try this one. The food was definitely below average. We tried the Mezze platter and it was the worst Mediterranean food I've had. Management was sufficiently apologetic and asked for feedback on the comments card. The thing that put me off was that the chef came out and started arguing with us and insisting that his food was perfect. He has no compulsion to implement our suggestions, but actually coming out and fighting was too much. Definitely not going again."
ww = "The Butter Chicken was not good at Al Kareem"
qq = "The sitting which is mostly outdoor is the prettiest you can come across in CP."
ss = "Spring rolls were just fine and their chicken drumsticks are hands down the best you can ever taste. However the noodles left me a bit unsatisfied and were below their usual standardself."
cc = "Going to Dunkin' Donuts is always a happy experience. Pleasant music and to add to charm is the dining area. A very filling variety of burgers, Naughty Lucy veg. is a must try. Wicked wraps are something unavoidable if you go there. Coffee tastes very nice, even the simplest Classic has its own taste and so are the milkshakes especially Fruit berry. Love it. Simply Awesome!"
vv = " This sagar ratna is very old restaurant serving delicious dahi vada & scrumptious south Indian food. This place is loosing its charm due to poor service & dull ambiance. Average place to visit."
aa = "The sofas are torn... Not well maintained. We took one couch that looked OK.. But then were asked to vacate it since it was reserved - even though there was no sign placed on the table that indicated reservation. The waiter's attitude was below the standards of a supposedly good restaurant chain. The food is overpriced for the quality and quantity... There is a minimum standard of presentation that is expected but was not there. Overall an avoidable experience, specially the CP outlet... I have heard the other outlets are good and hence was hugely disappointed coming to this one."



tokens = word_tokenize(rev6)
t = word_tokenize(rev2)

def main_func(review):
    final_score = {}
    compound_word_dic = {}
    compound_word_list = []
    neg_words = []
    sent = preprocess(review)
    dp,dd,names = typedependencies(sent,neg_words,compound_word_list)
    check_for_noun_adj(dp,dd,final_score,neg_words)
    print dd
    print '---------------Before root-------------'
    pprint.pprint(final_score)
    # if len(sent) < 3:
        # check_for_root(dp,dd,final_score,neg_words)
    print '--------------after root----------------'
    pprint.pprint(final_score)
    # print compound_word_list
    for i in range(len(compound_word_list)):
        compound_word_dic[compound_word_list[i]] = 1
    print '----------compound-----------'
    print compound_word_dic
    replace_with_compoundword(final_score,compound_word_dic)
    # print final_score


    r = []
    dish_score = {}
    for key,value in final_score.items():
        r.append(key)

    get_trained_classifier(r,final_score)
    pprint.pprint(final_score)
    food,service,ambience,cost,dish_list = final_scores(final_score)
    print food,service,ambience,cost
    # print dish_list
    dish_list_refined = []
    for x in range(len(dish_list)):
        if check_in_dic(dish_list[x]) != None:
            dish_list_refined.append(dish_list[x])
    print dish_list_refined
    return food,service,ambience,cost,dish_list_refined
    # get_dish_names(r,)

    # print dish_score

main_func(ww)



# getting_namedentity(sent)


# rev6,7{9}
# text = ('I went to the Pita Pit restaurant yesterday.The food was delicious but serving was horrible there.')
# text = ('London is good at studies but bad at sports.')

# good results-->> nrev,sample,rev4
# not good -->> nrev2
# bad -->> nrev3

    # print(output['sentences'][0]['parse'])
    # output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)
    # print(output)
    # output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
    # print(output)





# for w in t:
#   if re.search('ts$',w):
#       # print w
#       print 'hi'

# porter = nltk.PorterStemmer()
# print [porter.stem(t) for t in tokens]

# print t
# fdist = nltk.FreqDist(t)
# for word in sorted(fdist):
#   print('{}->{};'.format(word, fdist[word]))
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
# print stemmer3.lemmatize("loved")
# print stemmer.stem('lollies')
# print stemmer2.stem('lollies')
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
#   os.makedirs(path,0777)
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

# def getting_sentiment(word,pos):

#     for i in range(0,len(tagged)):
#         stemmer = WordNetLemmatizer()
#         x = stemmer.lemmatize(tagged[i][0])
#         if 'NN' in tagged[i][1] and len(swn.senti_synsets(x,'n')) > 0:
#             # pscore+=(list(swn.senti_synsets(tagged[i][0],'n'))[0]).pos_score() #positive score of a word
#                 # nscore+=(list(swn.senti_synsets(tagged[i][0],'n'))[0]).neg_score()  #negative score of a word
#             print str(tagged[i][0]) + ' (noun)---> ' + str(swn.senti_synsets(x,'n')[0].pos_score())
#         if 'JJ' in tagged[i][1] and len(swn.senti_synsets(x, 'a')) > 0:
#             print str(tagged[i][0]) + ' (adjective)---> ' + str(swn.senti_synsets(x,'a')[0].pos_score())

#         if 'VB' in tagged[i][0] and len(swn.senti_synsets(x,'v')) > 0:
#             print str(tagged[i][0]) + ' (verb)---> ' + str(swn.senti_synsets(x,'v')[0].pos_score())

#         if 'RB' in tagged[i][0] and len(swn.senti_synsets(x,'r')) > 0:
#             print str(tagged[i][0]) + ' (adverb)---> ' + str(swn.senti_synsets(x,'r')[0].pos_score())
