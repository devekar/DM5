from __future__ import division
import re
import sys
import timeit
from sample import split_dataset, split_and_write_dataset
import subprocess


# Read rules produced by the Off-The-Shelf program
# Skips rules for which consequent is not a label
# An element of rules is of the form:
# [label, [word1, word2, ...], support, confidence ]
def readRules(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    
    rules = []
    for line in lines:
        line = line.split()
        consequent = int(line[0])
        if consequent < 1156: continue
        rule = []
        rule.append(consequent); rule.append([])
        idx = 2
        for l in line[2:]:
            if "(" in l: break
            rule[1].append( int(l) )
            idx += 1

        sup = re.sub( '[(),]', '', line[idx]); rule.append( float(sup) )
        conf = re.sub( '[(),]', '', line[idx + 1]); rule.append( float(conf) )        
        rules.append(rule)


    return rules


# indexes store the index in each row of dataset where the labels start
def readDataset(path):
    f = open(path)
    lines = f.readlines()
    f.close()

    dataset = []
    for line in lines:
        line = map(int, line.split())
        dataset.append(line)

    return dataset


# Order rules by confidence
def orderRules(rules):
    rules.sort(key=lambda x: x[-1])
    rules.reverse()
    return rules


def isRuleApplicable(rule, row):
    for item in rule:
        if item not in row: return False
    return True
    

# Apply rules on training set and subsume them
def subsumeRules(rules, dataset):
    applicableCount = [0]*len(rules)
    
    for i, row in enumerate(dataset):
        for idx, rule in enumerate(rules):
            if rule[0] in row and isRuleApplicable(rule[1], row): 
                applicableCount[idx] += 1
                break
        if i%1000==0: print i

    rules1 = []
    for idx, count in enumerate(applicableCount):
        if count>0: rules1.append( rules[idx] )

    return rules1


# Predict labels by applying atmost K rules
def testRules(rules, dataset, K):
    labels_list = []

    for row in dataset:
        k = K #Only K rules must be applied i.e atmost K labels will generated
        labels = []
        for rule in rules:
            if isRuleApplicable(rule[1], row):
                labels.append(rule[0])
                k -= 1
                if not k: break

        labels_list.append(labels)

    return labels_list  


def getAccuracy(dataset, labels_list):
    matches = 0
    matches1 = 0
    for idx, labels in enumerate(labels_list):
        if not labels: continue
        row_match = 0
        actual_labels = [ x for x in dataset[idx] if x>=1156 ]

        if len(labels) < len(actual_labels):
            for label in labels:
                if label in actual_labels: row_match += 1
            matches1 += row_match/len(labels)
        else:
            for actual_label in actual_labels:
                if actual_label in labels: row_match += 1
            matches1 += row_match/len(actual_labels)

        if labels[0] in dataset[idx]: matches += 1


    print "Accuracy:", matches/len(labels_list)
    print "Accuracy by discussed method:", matches1/len(labels_list)


def main(argv):
    dataset_path = argv[1]    
    rules_path = argv[2]
    K = 5
    TEST_PERCENT = 20
    

    start_time = timeit.default_timer()
    # Read dataset from transaction file and split
    dataset = readDataset(dataset_path)
    train_set, test_set = split_dataset(TEST_PERCENT, dataset)
    print "Dataset size: ", len(train_set), len(test_set)

    # Write train and test sets
    split_and_write_dataset(train_set, test_set)

    # Invoke apriori program
    print ""
    apriori_command = ['./apriori', '-s2m2', '-c60', '-tr', 'train.csv', rules_path ]
    print apriori_command
    subprocess.call(apriori_command)
    print ""


    rules = readRules(rules_path)
    rules = orderRules(rules)
    print "No of rules before ordering:", len(rules)

    labels = set()
    for rule in rules:
        labels.add(rule[0])
    print "Labels before subsuming:", len(labels), labels

    subsume_time = -timeit.default_timer()
    subsumed_rules = subsumeRules(rules, train_set)
    print "No of rules after subsuming:", len(subsumed_rules)
    subsume_time += timeit.default_timer()
    print "Subsume time", str(subsume_time)


    labels = set()
    for rule in subsumed_rules:
        labels.add(rule[0])
    print "Labels after subsuming:", len(labels), labels


    labels_list = testRules(subsumed_rules, test_set, K)
    getAccuracy(test_set, labels_list)

    end_time = timeit.default_timer()
    print "Total time", str(end_time - start_time)



if __name__=="__main__": main(sys.argv)
