from main_file import main_func
from classifier import get_dish_lookup
import os
import csv



def check_dish(lis):
	result = []
	for i in range(len(lis)):
		support = 0
		name = lis[i]
		names = lis[i].split(" ")

		if name.lower() in dish_dic:
			support = support + 1

		if support == 0:
			for j in range(len(names)):
				if names[j].lower() in dish_dic:
					support = support + 1

		if support > 0:
			result.append([name,support])
	return result

def finding_score_of_file(filename,restname):
	handle = open('data/scores/' + filename,'r')
	reader = csv.DictReader(handle)
	ww = csv.writer(open('data/final_rest_scores.csv','a+'))
	food = 0.0
	fc = 0.0
	ambience = 0.0
	ac = 0.0
	service = 0.0
	sc = 0.0
	cost = 0.0
	cc = 0.0
	for row in reader:
		# print row
		if row['food'] != '-10000':
			food = food + float(row['food'])
			fc = fc + 1.0
		if row['cost'] != '-10000':
			cost = cost + float(row['cost'])
			cc = cc + 1.0
		if row['ambience'] != '-10000':
			ambience = ambience + float(row['ambience'])
			ac = ac + 1.0
		if row['service'] != '-10000':
			service = service + float(row['service'])
			sc = sc + 1.0
	try:
		print 'food-> ' +  str(food/fc)
		food = food/fc
	except:
		food = 'NA'
	try:
		print 'service-> ' + str(service/sc)
		service = service/sc
	except:
		service = 'NA'
	try:
		print 'ambience-> ' + str(ambience/ac)
		ambience = ambience/ac
	except:
		ambience = 'NA'
	try:
		print 'cost-> ' + str(cost/cc)
		cost = cost/cc
	except:
		cost = 'NA'
	ww.writerow([restname,food,ambience,service,cost])


def manipulate_file(filename):
	# filename = 'Cafe Dalal Street _reviews.csv'
	dish_dic = get_dish_lookup()

	handle = open('data/scores/' + filename[:-4] + '_scores.csv','w')
	writer = csv.writer(handle)
	writer.writerow(['sno','username','food','service','ambience','cost','rating','dishes'])

	hand = open('data/reviews/' + filename,'r')
	reader = csv.DictReader(hand)
	count = 2
	for row in reader:
		review = row['Review']
		name = row['Username']
		rating = row['Rating']
		try:
			food,service,ambience,cost,dishes = main_func(review)
			dish_li = check_dish(dishes)
			writer.writerow([count,name,food,service,ambience,cost,rating,dish_li])
			print food,service,ambience,cost
		except:
			print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		count = count + 1


# manipulate_file('Jungle Jamboree _reviews.csv')
finding_score_of_file('Jungle Jamboree _reviews_scores.csv','jungle jumboore')