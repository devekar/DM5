
def split_supconf(filename):
	a = filename[4:len(filename)-7]
	a = a.split('_')
	sup = float(a[0])
	conf = int(a[1])
	clusters = int(a[2])
	return sup, conf, clusters
	
def process_line(line):
	a = line.split(':')
	sup, conf, clusters = split_supconf(a[0])
	time = float(a[2])
	return sup, conf, clusters, time

dic = {}

f = open("testingTime")
lines = f.readlines()
f.close()
for line in lines:
	sup, conf, clusters, testTime = process_line(line)
	if sup not in dic:
		dic[sup] = {}
	if conf not in dic[sup]:
		dic[sup][conf] = {}
	if clusters not in dic[sup][conf]:
		dic[sup][conf][clusters] = {}
	dic[sup][conf][clusters]['testTime'] = testTime
	#print sup, conf, testTime


f = open("trainingTime")
lines = f.readlines()
f.close()
for line in lines:
	sup, conf, clusters, trainTime = process_line(line)
	dic[sup][conf][clusters]['trainTime'] = trainTime
	#print sup, conf, trainTime


f = open("fmeasure")
lines = f.readlines()
f.close()
for i in xrange(len(lines)/2):
	l = lines[2*i:2*(i+1)]
	for idx, line in enumerate(l):
		sup, conf, clusters, fm = process_line(line)
		if idx==0:
			dic[sup][conf][clusters]['fm1'] = fm
		elif idx==1:
			dic[sup][conf][clusters]['fm2'] = fm
		#print sup, conf, acc


f = open("accuracy")
lines = f.readlines()
f.close()
for i in xrange(len(lines)/4):
	l = lines[4*i:4*(i+1)]
	for idx, line in enumerate(l):
		sup, conf, clusters, acc = process_line(line)
		if idx==0:
			dic[sup][conf][clusters]['acc1'] = acc
		elif idx==1:
			dic[sup][conf][clusters]['acc2'] = acc
		elif idx==2:
			dic[sup][conf][clusters]['acc3'] = acc
		elif idx==3:
			dic[sup][conf][clusters]['acc4'] = acc
		#print sup, conf, acc


for cl in [8,16]:
	f = open("graph_input_"+str(cl)+".dat", "w")
	s = "Support Confidence Acc1 Acc2 Acc3 Acc4 Fmeasure1 Fmeasure2 TrainTime TestTime\n"
	f.write(s)
	for sup in dic: 
		for conf in dic[sup]:
			#print sup, conf, dic[sup][conf]
			d = dic[sup][conf][cl]
			s = str(sup) + " " + str(conf) + " " + str(d['acc1']) + " " + str(d['acc2']) + " "
			s += str(d['acc3']) + " " + str(d['acc4']) + " " + str(d['fm1']) + " " + str(d['fm2'])
			s += " " + str(d['trainTime']) + " " + str(d['testTime']) + "\n"
			f.write(s)


