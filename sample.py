from __future__ import division
import sys
import random
# from parseRules import readDataset

def read_dataset(dmpath, tmpath):
	f = open(dmpath)
	dm = f.readlines()
	f.close()
	f = open(tmpath)
	tmlines = f.readlines()
	f.close()

	tm = []
	for line in tmlines:
		line = map(int, line.split())
		tm.append(line)

	return dm, tm


def split_dataset(test_percent, dm_full, tm):
	dm = dm_full[2:]
	dataset_len = len(tm)
	train_indices = range(dataset_len)
	test_indices = []
	test_set_len = test_percent * dataset_len // 100
	for i in xrange(test_set_len):
		random_index = random.randint(0, dataset_len - i - 1)
		#print random_index, len(train_indices)
		n = train_indices.pop(random_index)
		test_indices.append(n)
	test_indices.sort()
	return train_indices, test_indices


def write_train_test_files(train_indices, test_indices, dm, tm):
	title_lines = []
	title_lines.append(dm.pop(0))
	title_lines.append(dm.pop(1))
	train_file = open("dm_train.csv", "w")
	train_file.write(title_lines[0])
	train_file.write(title_lines[1])
	for i in train_indices:
		train_file.write(dm[i])
	train_file.close()
	test_file = open("dm_test.csv", "w")
	test_file.write(title_lines[0])
	test_file.write(title_lines[1])
	for i in test_indices:
		test_file.write(dm[i])
	test_file.close()

	train_file = open("tm_train.csv", "w")
	for i in train_indices:
		line = tm[i]
		train_file.write(' '.join(map(str,line)) + '\n')
	train_file.close()
	test_file = open("tm_test.csv", "w")
	for i in test_indices:
		line = tm[i]
		test_file.write(' '.join(map(str,line)) + '\n')
	test_file.close()


#### MAIN ####
dm, tm = read_dataset(sys.argv[1], sys.argv[2])
train_ind, test_ind = split_dataset(int(sys.argv[3]), dm, tm)
write_train_test_files(train_ind, test_ind, dm, tm)

