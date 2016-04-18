def final_scores(dic):
	food = 0
	fc = 0
	ambience = 0
	ac = 0
	service = 0
	sc = 0
	cost = 0
	cc = 0
	for key,value in dic.items():
		lis = value
		if lis[3] == 'food':
			food = food + lis[0]
			fc = fc + 1
		elif lis[3] == 'ambience':
			ambience = ambience + lis[0]
			ac = ac + 1
		elif lis[3] == 'cost':
			cost = cost + lis[0]
			cc = cc + 1
		elif lis[3] == 'service':
			service = service + lis[0]
			sc = sc + 1
	try:
		print 'food-> ' +  str(food/fc)
	except:
		pass
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


