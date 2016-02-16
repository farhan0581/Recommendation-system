import requests
import json
import csv
import pprint
from bs4 import BeautifulSoup
import os,sys

# finding the restaurants at a locality
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
			'Connection':'keep-alive','Host':'www.zomato.com',
				'Referer':'https://www.zomato.com/'}

def crawl_rest(url_list,name_list):
	page = 0
	for i in range(len(url_list)):

		formdata = {'entity_id':str(url_list[i]),'profile_action':'reviews-dd','page':str(page),'limit':'5'}

		data = requests.post('https://www.zomato.com/php/social_load_moreself.php',headers=headers,data=formdata)
		page = page + 1
		soup = BeautifulSoup(data.text)






search_string = raw_input('enter the search string....')
data = requests.get('https://www.zomato.com/php/liveSuggest.php?type=keyword&search_bar=1&q='+ search_string +'&online_ordering=&search_city_id=1&entity_id=1&entity_type=city',headers=headers)
soup = BeautifulSoup(json.loads(data.text))
print '------these are the options available-------'
available = []
for item in soup.findAll('li'):
	x = item.find('div',{'class':'keywords-dd-l'})
	y = item.find('a')
	available.append(y['href'])
	print x.getText()
i = raw_input('which option??')

# getting the id for restuarant
data = requests.get(available[int(i)-1],headers = headers)
soup = BeautifulSoup(data.text)

sites = []
rest_list = []
for item in soup.findAll('li',{'class':'js-search-result-li'}):
	rest_id = item['data-res_id']
	x = item.find('a',{'class':'result-title'})
	rest_name = x.getText()
	addr = x['href']
	sites.append(str(rest_id))
	rest_list.append(str(rest_name))

