def final_scores(dic):
	food = 0.0
	fc = 0.0
	ambience = 0.0
	ac = 0.0
	service = 0.0
	sc = 0.0
	cost = 0.0
	cc = 0.0
	for key,value in dic.items():
		lis = value
		if lis[4] == 'food':
			food = food + float(lis[0])
			fc = increment(fc,lis[3])
		elif lis[4] == 'ambience':
			ambience = ambience + float(lis[0])
			ac = increment(ac,lis[3])
		elif lis[4] == 'cost':
			cost = cost + float(lis[0])
			cc = increment(cc,lis[3]) 
		elif lis[4] == 'service':
			service = service + float(lis[0])
			sc = increment(sc,lis[3])
	print fc
	print ac
	try:
		print 'food-> ' +  str(food/fc)
	except:
		print 'canno'
	try:
		print 'service-> ' + str(service/sc)
	except:
		pass
	try:
		print 'ambience-> ' + str(ambience/ac)
	except:
		pass
	try:
		print 'cost-> ' + str(cost/cc)
	except:
		pass


def increment(value,flag):
	if flag == 0:
		value = value + 0.3
	elif flag == 1:
		value = value + 0.7
	elif flag == 2:
		value = value + 1

	return value

def get_dish_names():
	pass