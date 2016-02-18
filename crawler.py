import requests
import json
import csv
import pprint
from bs4 import BeautifulSoup
import os,sys
import time

# finding the restaurants at a locality
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
				'Referer':'https://www.zomato.com/','x-requested-with':'XMLHttpRequest'}

def crawl_rest(url_list,name_list):
	
	base_path = os.path.dirname(os.path.dirname(__file__))
	path = os.path.join(base_path, "Recommendation-system","data")
	file_base = path + '/'
	for i in range(len(url_list)):
		count = 1
		page = 0
		print '=============================================================='
		print name_list[i]
		try:
			handle = open('data/'  +str(name_list[i]) + '_reviews.csv','w')
		except:
			print ' cannot make file....'
		writer = csv.writer(handle)
		writer.writerow(['Username','Review','Rating','Total_reviews','Followers','Expert_level'])
		time.sleep(5)
		while count > 0:
			formdata = {'entity_id':str(url_list[i]),'profile_action':'reviews-dd','page':str(page),'limit':'10'}
			headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
				'Referer':'https://www.zomato.com/','x-requested-with':'XMLHttpRequest'}
			data = requests.post('https://www.zomato.com/php/social_load_more.php',headers=headers,data=formdata)
			jdata = data.json()
			count = jdata['left_count']
			# count = -1
			page = page + 1
			soup = BeautifulSoup(jdata['html'])
			for item in soup.findAll('div',{'itemprop':'review'}):
				x = item.find('div',{'class':'rev-text'})
				y = item.find('div',{'class':'snippet__name'})
				try:	
					name = y.find('span').getText()
				except:
					name = 'Not Known'
				z = item.find('div',{'class':'snippet__stats'})
				try:
					reviews = (z.find('span',{'class':'snippet__reviews'})).getText()
				except:
					reviews = 0
				try:
					followers = (z.find('span',{'class':'snippet__followers'})).getText()
				except:
					followers = 0
				try:
					expert = (z.find('span',{'class':'snippet__expertise'})).getText()
				except:
					expert = '??'
				name = name.strip()
				reviews = str(reviews).strip()
				followers = str(followers).strip()
				expert = expert.strip()
				review = (x.getText()).encode("ascii","ignore")
				# p/rint str(review).lstrip(' \t\n\r')
				review = " ".join(review.split())
				rating = x.find('div',{'class':'ttupper'})
				rating = rating['aria-label']
				name = name.encode("ascii","ignore")
				print '----------------'
				writer.writerow([name,review,rating,reviews,followers,expert])







# search_string = raw_input('enter the search string....')
# data = requests.get('https://www.zomato.com/php/liveSuggest.php?type=keyword&search_bar=1&q='+ search_string +'&online_ordering=&search_city_id=1&entity_id=1&entity_type=city',headers=headers)
# soup = BeautifulSoup(json.loads(data.text))
# print '------these are the options available-------'
# available = []
# for item in soup.findAll('li'):
# 	x = item.find('div',{'class':'keywords-dd-l'})
# 	y = item.find('a')
# 	available.append(y['href'])
# 	print x.getText()
# i = raw_input('which option??')

# # getting the id for restuarant
# data = requests.get(available[int(i)-1],headers = headers)
# soup = BeautifulSoup(data.text)

# sites = []
# rest_list = []
# for item in soup.findAll('li',{'class':'js-search-result-li'}):
# 	rest_id = item['data-res_id']
# 	x = item.find('a',{'class':'result-title'})
# 	rest_name = x.getText()
# 	addr = x['href']
# 	sites.append(str(rest_id))
# 	rest_list.append(str(rest_name))

sites = [  '302878', '7855', '900', '18124357', '18157384', '18222559', '309586']

rest_list =[   'Cha Bar ',
 "Dunkin' Donuts ", 'Saravana Bhavan ', 'Garam Dharam ', 'Jungle Jamboree ', '{Niche} - Lounge & Bistro ', 'Kinbuck 2 ']

crawl_rest(sites,rest_list)

