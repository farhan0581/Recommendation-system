from main_file import main_func
import os
import csv

handle = open('data/scores.csv','w')
writer = csv.writer(handle)
writer.writerow(['sno.','food','service','ambience','cost'])

hand = open('data/reviews/test.csv','r')
reader = csv.DictReader(hand)
count = 1
for row in reader:
	review = row['Review']
	# try:
	food,service,ambience,cost = main_func(review)
	writer.writerow([count,food,service,ambience,cost])
	print food,service,ambience,cost
# except:
	print '==============='
	count = count + 1
