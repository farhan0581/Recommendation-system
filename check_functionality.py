# import re
# import re
# string1 = "use code wib125 to avail"
# x = int(re.search(r'\d+', string1).group())
# # y = map(int, re.findall(r'\d+', string1))
# # print x
# # dd = {'z':2,'farhan':100,'khzan':3}
# # for key in dd:
# # 	if key in 'my name is farhankhan':
# # 		print key

# if x > 100:
# 	print 'Avail flat %s'%(x) + ' Rs off via swiggy on %s'%(x)

# print 'Avail %s'%(x) + '% off via swiggy'

# s = 'NNS'
# if 'NNS' in s:
# 	print 'gdfg'
# cp  -i /home/farhan/Downloads/abdul_ec2.pem ubuntu@ec2-54-218-84-194.us-west-2.compute.amazonaws.com:/home/ubuntu/stanford-parser-full-2015-04-20.zip /home/farhan/Desktop/

# torify scp -i farhan_test.pem ubuntu@ec2-54-201-105-208.us-west-2.compute.amazonaws.com:/home/ubuntu/stanford-parser-full-2015-04-20.zip /home/farhan/Desktop/

import requests
import jsonrpclib
import pprint
from simplejson import loads
server = jsonrpclib.Server("http://localhost:8080")


# rev= "Please go there for the ambience but also for the delicious food. The sitting which is mostly outdoor is the prettiest you can come across in CP. The drinks are a must have. The Giardino served in a lamp is beautiful and refreshing. The Nutty Jack is a delightful drink Bailey's, Jack Daniels served with peanut butter. Aam Papad Caprioska a perfect summer drink with chunks of aam papad. Starters: I absolutely recommend the Ganna Chicken a kebab wrapped on small sticks of sugar cane. Aam Aadmi Chicken yummy and spicy, this us served in a steel tiffin like old times. Chilli Paneer Ghosla is a nest of fried noodles stuffed with chilli panner topped with cheese slices. Red Gull Croquettes are cheese and potato croquettes served with a special redbull sauce. Main Course: the main course is filling and desi at heart. The Traphalgar Chicken Curry is perfectly spiced chicken curry. The biryani is on my must eat list. Desserts : the desserts are molecular gastronomy style. So we had a special UC Cake which is a cake and icing dipped in liquid nitrogen and topped with sauce. Molecular Lollies too are made with liquid nitrogen."
rev = "I went to the Pita Pit restaurant yesterday.The food was delicious but serving was horrible there."
result = loads(server.parse(rev))
x = result['sentences']
for i in range(len(x)):
	y = x[i]['dependencies']
	for j in range(len(y)):
		print y[j][0] + '-->'+ ',' + y[j][1] + ','  + y[j][2] + ',' + y[j][3] + ',' + y[j][4]
pprint.pprint(result)




# requests.get('wget --post-data 'the quick brown fox jumped over the lazy dog' 'localhost:9000/?properties={"tokenize.whitespace": "true", "annotators": "tokenize,ssplit,pos,ner,dcoref", "outputFormat": "json"}' -O -')
# x = [[{"index":0,"parse":"(ROOT\n  (S\n    (NP (DT the) (JJ quick) (JJ brown) (NN fox))\n    (VP (VBD jumped)\n      (PP (IN over)\n        (NP (DT the) (JJ lazy) (NN dog))))))","basic-dependencies":[{"dep":"ROOT","governor":0,"governorGloss":"ROOT","dependent":5,"dependentGloss":"jumped"},{"dep":"det","governor":4,"governorGloss":"fox","dependent":1,"dependentGloss":"the"},{"dep":"amod","governor":4,"governorGloss":"fox","dependent":2,"dependentGloss":"quick"},{"dep":"amod","governor":4,"governorGloss":"fox","dependent":3,"dependentGloss":"brown"},{"dep":"nsubj","governor":5,"governorGloss":"jumped","dependent":4,"dependentGloss":"fox"},{"dep":"case","governor":9,"governorGloss":"dog","dependent":6,"dependentGloss":"over"},{"dep":"det","governor":9,"governorGloss":"dog","dependent":7,"dependentGloss":"the"},{"dep":"amod","governor":9,"governorGloss":"dog","dependent":8,"dependentGloss":"lazy"},{"dep":"nmod","governor":5,"governorGloss":"jumped","dependent":9,"dependentGloss":"dog"}],"collapsed-dependencies":[{"dep":"ROOT","governor":0,"governorGloss":"ROOT","dependent":5,"dependentGloss":"jumped"},{"dep":"det","governor":4,"governorGloss":"fox","dependent":1,"dependentGloss":"the"},{"dep":"amod","governor":4,"governorGloss":"fox","dependent":2,"dependentGloss":"quick"},{"dep":"amod","governor":4,"governorGloss":"fox","dependent":3,"dependentGloss":"brown"},{"dep":"nsubj","governor":5,"governorGloss":"jumped","dependent":4,"dependentGloss":"fox"},{"dep":"case","governor":9,"governorGloss":"dog","dependent":6,"dependentGloss":"over"},{"dep":"det","governor":9,"governorGloss":"dog","dependent":7,"dependentGloss":"the"},{"dep":"amod","governor":9,"governorGloss":"dog","dependent":8,"dependentGloss":"lazy"},{"dep":"nmod:over","governor":5,"governorGloss":"jumped","dependent":9,"dependentGloss":"dog"}],"collapsed-ccprocessed-dependencies":[{"dep":"ROOT","governor":0,"governorGloss":"ROOT","dependent":5,"dependentGloss":"jumped"},{"dep":"det","governor":4,"governorGloss":"fox","dependent":1,"dependentGloss":"the"},{"dep":"amod","governor":4,"governorGloss":"fox","dependent":2,"dependentGloss":"quick"},{"dep":"amod","governor":4,"governorGloss":"fox","dependent":3,"dependentGloss":"brown"},{"dep":"nsubj","governor":5,"governorGloss":"jumped","dependent":4,"dependentGloss":"fox"},{"dep":"case","governor":9,"governorGloss":"dog","dependent":6,"dependentGloss":"over"},{"dep":"det","governor":9,"governorGloss":"dog","dependent":7,"dependentGloss":"the"},{"dep":"amod","governor":9,"governorGloss":"dog","dependent":8,"dependentGloss":"lazy"},{"dep":"nmod:over","governor":5,"governorGloss":"jumped","dependent":9,"dependentGloss":"dog"}],"tokens":[{"index":1,"word":"the","originalText":"the","lemma":"the","characterOffsetBegin":0,"characterOffsetEnd":3,"pos":"DT","ner":"O","speaker":"PER0"},{"index":2,"word":"quick","originalText":"quick","lemma":"quick","characterOffsetBegin":4,"characterOffsetEnd":9,"pos":"JJ","ner":"O","speaker":"PER0"},{"index":3,"word":"brown","originalText":"brown","lemma":"brown","characterOffsetBegin":10,"characterOffsetEnd":15,"pos":"JJ","ner":"O","speaker":"PER0"},{"index":4,"word":"fox","originalText":"fox","lemma":"fox","characterOffsetBegin":16,"characterOffsetEnd":19,"pos":"NN","ner":"O","speaker":"PER0"},{"index":5,"word":"jumped","originalText":"jumped","lemma":"jump","characterOffsetBegin":20,"characterOffsetEnd":26,"pos":"VBD","ner":"O","speaker":"PER0"},{"index":6,"word":"over","originalText":"over","lemma":"over","characterOffsetBegin":27,"characterOffsetEnd":31,"pos":"IN","ner":"O","speaker":"PER0"},{"index":7,"word":"the","originalText":"the","lemma":"the","characterOffsetBegin":32,"characterOffsetEnd":35,"pos":"DT","ner":"O","speaker":"PER0"},{"index":8,"word":"lazy","originalText":"lazy","lemma":"lazy","characterOffsetBegin":36,"characterOffsetEnd":40,"pos":"JJ","ner":"O","speaker":"PER0"},{"index":9,"word":"dog","originalText":"dog","lemma":"dog","characterOffsetBegin":41,"characterOffsetEnd":44,"pos":"NN","ner":"O","speaker":"PER0"}]}],"corefs":{"1":[{"id":1,"text":"the quick brown fox","type":"NOMINAL","number":"SINGULAR","gender":"MALE","animacy":"ANIMATE","startIndex":1,"endIndex":5,"sentNum":1,"position":[1,1],"isRepresentativeMention":true}],"2":[{"id":2,"text":"the lazy dog","type":"NOMINAL","number"}]]

li = ['1','2','3','4','5']
print li[2:3]