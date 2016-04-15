import requests
import json
import csv
import pprint
from bs4 import BeautifulSoup
import os,sys,re

# finding the restaurants at a locality
# headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
# 			(KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
# 			'Connection':'keep-alive','Host':'www.zomato.com',
# 				'Referer':'https://www.zomato.com/'}


# url_list = [18070476]
# i = 0
# page = 0
# count = 10
# while count > 0:

# 	formdata = {'entity_id':'18070476','profile_action':'reviews-dd','page':str(page),'limit':'30'}

# 	data = requests.post('https://www.zomato.com/php/social_load_more.php',headers=headers,data=formdata)
# 	jdata = data.json()
# 	# count = jdata['left_count']
# 	count = -1
# 	page = page + 1
# 	soup = BeautifulSoup(jdata['html'])
# 	for item in soup.findAll('div',{'itemprop':'review'}):
# 		x = item.find('div',{'class':'rev-text'})
# 		y = item.find('div',{'class':'snippet__name'})
# 		try:	
# 			name = y.find('span').getText()
# 		except:
# 			name = 'Not Known'
# 		z = item.find('div',{'class':'snippet__stats'})
# 		try:
# 			reviews = (z.find('span',{'class':'snippet__reviews'})).getText()
# 		except:
# 			reviews = 0
# 		try:
# 			followers = (z.find('span',{'class':'snippet__followers'})).getText()
# 		except:
# 			followers = 0
# 		try:
# 			expert = (z.find('span',{'class':'snippet__expertise'})).getText()
# 		except:
# 			expert = '??'
# 		print name.strip()
# 		print reviews
# 		print followers
# 		print expert.strip()
# 		review = (x.getText()).encode("ascii","ignore")
# 		# p/rint str(review).lstrip(' \t\n\r')
# 		print " ".join(review.split())
# 		rating = x.find('div',{'class':'ttupper'})
# 		print rating['aria-label']
# 		print '----------------'
# data = {'filter':'{"veg":"0","deliverable":["101","DLF Cyber City"]}'}

# r = requests.post('http://ec2-54-201-233-108.us-west-2.compute.amazonaws.com/production/main',data=data)
# print r.headers
# dic = {'my':1,'farhan':2}
# lis = ['my','name','is','chicken curry']
# # m = re.search(r'curr',lis)
# if 'chicken' in lis:
# 	print 'yes'
	
# for k,v in dic.items():
# 	if 'far' in k:
# 		print k

writer = csv.writer(open('data/final_train.csv','w'))

handle = open('/home/farhan/manual_test_data.csv','r')
reader = csv.DictReader(handle)
for row in reader:
	writer.writerow([row['Review'].strip(),row['Modified Tag']])
handle.close()
handle = open('data/farhan.csv','r')
reader = csv.DictReader(handle)
for row in reader:
	writer.writerow([row['review'].strip(),'cost'])
handle.close()
handle = open('data/shabaz.csv','r')
reader = csv.DictReader(handle)
for row in reader:
	writer.writerow([row['review'].strip(),'cost'])
handle.close()
handle = open('data/habib.csv','r')
reader = csv.DictReader(handle)
for row in reader:
	writer.writerow([row['review'].strip(),'cost'])
handle.close()

