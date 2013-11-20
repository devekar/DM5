from __future__ import division
import sys
import random
# from parseRules import readDataset

def split_dataset(test_percent, dataset):
	test_set = []
	dataset_len = len(dataset)
	test_set_len = test_percent * dataset_len // 100
	for i in xrange(test_set_len):
		random_index = random.randint(0, dataset_len - i - 1)
		test_set.append(dataset.pop(random_index))
	return dataset, test_set


def split_and_write_dataset(train_set, test_set):
	train_file = open("train.csv", "w")
	for item in train_set:
		train_file.write(' '.join(map(str,item)) + '\n')
	train_file.close()
	test_file = open("test.csv", "w")
	for item in test_set:
		test_file.write(' '.join(map(str,item)) + '\n')
	test_file.close()


#### MAIN ####
# split_and_write_dataset(20, sys.argv[1])
