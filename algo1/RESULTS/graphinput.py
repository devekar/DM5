
def split_supconf(filename):
	a = filename[4:len(filename)-7]
	a = a.split('_')
	sup = float(a[0])
	conf = int(a[1])
	return sup, conf
	
def process_line(line):
	a = line.split(':')
	sup, conf = split_supconf(a[0])
	time = float(a[2])
	return sup, conf, time

dic = {}

f = open("testingTime")
lines = f.readlines()
f.close()
for line in lines:
	sup, conf, testTime = process_line(line)
	if sup not in dic:
		dic[sup] = {}
	if conf not in dic[sup]:
		dic[sup][conf] = {}
	dic[sup][conf]['testTime'] = testTime
	#print sup, conf, testTime


f = open("trainingTime")
lines = f.readlines()
f.close()
for line in lines:
	sup, conf, trainTime = process_line(line)
	dic[sup][conf]['trainTime'] = trainTime
	#print sup, conf, trainTime


f = open("fmeasure")
lines = f.readlines()
f.close()
for i in xrange(len(lines)/2):
	l = lines[2*i:2*(i+1)]
	for idx, line in enumerate(l):
		sup, conf, fm = process_line(line)
		if idx==0:
			dic[sup][conf]['fm1'] = fm
		elif idx==1:
			dic[sup][conf]['fm2'] = fm
		#print sup, conf, acc


f = open("accuracy")
lines = f.readlines()
f.close()
for i in xrange(len(lines)/4):
	l = lines[4*i:4*(i+1)]
	for idx, line in enumerate(l):
		sup, conf, acc = process_line(line)
		if idx==0:
			dic[sup][conf]['acc1'] = acc
		elif idx==1:
			dic[sup][conf]['acc2'] = acc
		elif idx==2:
			dic[sup][conf]['acc3'] = acc
		elif idx==3:
			dic[sup][conf]['acc4'] = acc
		#print sup, conf, acc


f = open("graph_input.dat", "w")
s = "Support\tConfidence\tAcc1\tAcc2\tAcc3\tAcc4\tFmeasure1\tFmeasure2\tTrainTime\tTestTime\n"
f.write(s)
for sup in dic: 
	for conf in dic[sup]:
		#print sup, conf, dic[sup][conf]
		d = dic[sup][conf]
		s = str(sup) + "\t" + str(conf) + "\t" + str(d['acc1']) + "\t" + str(d['acc2']) + "\t"
		s += str(d['acc3']) + "\t" + str(d['acc4']) + "\t" + str(d['fm1']) + "\t" + str(d['fm2'])
		s += "\t" + str(d['trainTime']) + "\t" + str(d['testTime']) + "\n"
		f.write(s)


