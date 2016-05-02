from main_file import main_func
from classifier import get_dish_lookup
import os
import csv

filename = 'test.csv'
dish_dic = get_dish_lookup()

def check_dish(lis):
	result = []
	for i in range(len(lis)):
		support = 0
		name = lis[i]
		names = lis[i].split(" ")
		print names

		if name.lower() in dish_dic:
			support = support + 1

		if support == 0:
			for j in range(len(names)):
				if names[j].lower() in dish_dic:
					support = support + 1

		if support > 0:
			result.append([name,support])
	return result


# li = ['Butter chicken','dal makhni']
# print check_dish(li)

handle = open('data/' + filename[:-4] + '_scores.csv','w')
writer = csv.writer(handle)
writer.writerow(['sno.','food','service','ambience','cost'])

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
