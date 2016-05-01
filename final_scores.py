def final_scores(dic):
	food = 0.0
	fc = 0.0
	ambience = 0.0
	ac = 0.0
	service = 0.0
	sc = 0.0
	cost = 0.0
	cc = 0.0
	dishes = []

	for key,value in dic.items():
		lis = value
		if lis[5] == 'food' and lis[0] != 0.0:
			food = food + float(lis[0]) * float(lis[3])
			fc = increment(fc,lis[3])
			if float(lis[3]) > 0.8:
				dishes.append(key)

		elif lis[5] == 'ambience'  and lis[0] != 0.0:
			ambience = ambience + float(lis[0]) * float(lis[3])
			ac = increment(ac,lis[3])
		elif lis[5] == 'cost'  and lis[0] != 0.0:
			cost = cost + float(lis[0]) * float(lis[3])
			cc = increment(cc,lis[3]) 
		elif lis[5] == 'service' and lis[0] != 0.0:
			service = service + float(lis[0]) * float(lis[3])
			sc = increment(sc,lis[3])
	print fc
	print ac
	try:
		print 'food-> ' +  str(food/fc)
		food = food/fc
	except:
		food = -10000
	try:
		print 'service-> ' + str(service/sc)
		service = service/sc
	except:
		service = -10000
	try:
		print 'ambience-> ' + str(ambience/ac)
		ambience = ambience/ac
	except:
		ambience = -10000
	try:
		print 'cost-> ' + str(cost/cc)
		cost = cost/cc
	except:
		cost = -10000
	return food,service,ambience,cost,dishes


def increment(value,flag):
	if flag == 0.2:
		value = value + 0.2
	elif flag == 0.8:
		value = value + 0.8
	elif flag == 1:
		value = value + 1

	return value

def get_dish_names():
	pass