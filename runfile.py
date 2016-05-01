from main_file import main_func
import os
import csv

filename = 'test.csv'

handle = open('data/' + filename + '_scores.csv','w')
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
		writer.writerow([count,name,food,service,ambience,cost,rating,dishes])
		print food,service,ambience,cost
	except:
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
	count = count + 1
