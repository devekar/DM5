from __future__ import division
import re
import sys
import timeit

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
    indexes = []    
    for line in lines:
        line = map(int, line.split())
        idx = next(x[0] for x in enumerate(line) if x[1] >= 1156 )
        dataset.append(line)
        indexes.append(idx)

    return dataset, indexes


# Order rules by confidence
def orderRules(rules):
    rules.sort(key=lambda x: x[-1])
    rules.reverse()
    return rules


def isRuleApplicable(rule, row):
    for item in rule:
        if item not in row: return False
    return True
    

# Apply rules on training set and prune them
def pruneRules(rules, dataset):
    applicableCount = [0]*len(rules)
    
    for i, row in enumerate(dataset):
        for idx, rule in enumerate(rules):
            if rule[0] in row and isRuleApplicable(rule[1], row): applicableCount[idx] += 1
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
            if k==0: break
            if isRuleApplicable(rule[1], row):
                k -= 1
                labels.append(rule[0])
        labels_list.append(labels)

    return labels_list  


def getAccuracy(dataset, labels_list, indexes):
    matches = 0
    matches1 = 0
    for idx, labels in enumerate(labels_list):
        if not labels: continue
        row_match = 0
        actual_labels = dataset[idx][ indexes[idx]: ]

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
    rules = readRules(rules_path)
    rules = orderRules(rules)

    dataset, indexes = readDataset(dataset_path)
    train_set = dataset[: len(dataset)*8//10]
    test_set = dataset[len(dataset)*8//10:]
    test_indexes = indexes[len(dataset)*8//10:]

    pruned_rules = pruneRules(rules, train_set)
    print len(rules), rules[0]
    print len(pruned_rules)

    labels_list = testRules(pruned_rules, test_set, K)
    getAccuracy(test_set, labels_list, test_indexes)





if __name__=="__main__": main(sys.argv)
