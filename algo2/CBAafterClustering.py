from __future__ import division
import re
import sys
import timeit
import itertools
import subprocess
import cluster_code as cc
from cluster_tm import create_cluster_tms


RULES_PATH = "rules.tmp"
APRIORI_INPUT_PATH = "input.tmp"
TOTAL_ITERATIONS = 5
K = 5


# indexes store the index in each row of dataset where the labels start
def readDataset(path):
    with open(path) as f: lines = f.readlines()

    dataset = []
    for line in lines:
        dataset.append( map(int, line.split()) )

    return dataset


# Split features and labels from dataset
def separateFeaturesAndLabels(dataset):
    labels_list = []
    feature_set = []
    for row in dataset:
        idx = next( x[0] for x in enumerate(row) if x[1] >= 1156 )
        feature_set.append( row[:idx] )
        labels_list.append( row[idx:] )

    return feature_set, labels_list


# Read rules produced by the Off-The-Shelf program
# Skips rules for which consequent is not a label
# The rule in file is of the form:
# label <- word1 word2 ... wordi (support) (confidence)

# An element of rules returned is of the form:
# [label, [word1, word2, ...], support, confidence ]
def readRules(path):
    with open(path) as f: lines = f.readlines()
    
    rules = []
    for line in lines:
        line = line.split()
        consequent = int(line[0])
        if consequent < 1156: continue
        rule = []
        rule.append(consequent); rule.append([])

        rule[1] = map(int, line[2:-2])

        valid_rule_flag = True
        for r in rule[1]:
            if r >= 1156: 
                valid_rule_flag = False
                break
        if not valid_rule_flag: continue

        sup = re.sub( '[(),]', '', line[-2]); rule.append( float(sup) )
        conf = re.sub( '[(),]', '', line[-1]); rule.append( float(conf) )        
        rules.append(rule)

    return rules


# Order rules by confidence
def orderRules(rules):
    rules.sort(key=lambda x: x[-1])
    rules.reverse()
    return rules


# Check if antecedent of rule is present in row
def isRuleApplicable(rule, row):
    for item in rule:
        if item not in row: return False
    return True
    

# Apply rules on training set and subsume them
def subsumeRules(rules, features_list, labels_list):
    applicableCount = [False]*len(rules)               # No of transactions, the rule was applicable to
    transactionsCovered = [False]*len(features_list)   # Whether transaction was covered

    for i, features in enumerate(features_list):
        for idx, rule in enumerate(rules):
            if rule[0] in labels_list[i] and isRuleApplicable(rule[1], features): 
                applicableCount[idx] = True
                transactionsCovered[i] = True
                break

    # Create a list of rules which covered transaction, disregard ones which did not
    subsumed_rules = []
    for idx, flag in enumerate(applicableCount):
        if flag: subsumed_rules.append( rules[idx] )

    # Create a dataset containing the uncovered transactions
    uncovered_features_list = []; uncovered_labels_list = []
    for idx, flag in enumerate(transactionsCovered):
        if not flag: 
            uncovered_features_list.append( features_list[idx] )
            uncovered_labels_list.append( labels_list[idx] )

    return subsumed_rules, uncovered_features_list, uncovered_labels_list



# Predict labels by applying atmost K rules
def testRules(rules, test_feature_set):
    predicted_labels_list = []

    for row in test_feature_set:
        k = K #Only K rules must be applied i.e atmost K labels will generated
        labels = set()
        for rule in rules:
            if isRuleApplicable(rule[1], row):
                labels.add(rule[0])
                k -= 1
                if not k: break

        predicted_labels_list.append(labels)

    return predicted_labels_list  


# Try to predict as many labels as actually present
def testRulesWithVariableK(rules, test_feature_set, test_labels_list):
    labels_list = []

    for idx, row in enumerate(test_feature_set):
        k =  len(test_labels_list) #Apply rules until k labels generated
        labels = set()
        for rule in rules:
            if isRuleApplicable(rule[1], row):
                labels.add(rule[0])
                if len(labels)==k: break

        labels_list.append(labels)

    return labels_list  


# Accuracy method for K-rules testing
def getAccuracy(test_labels_list, predicted_labels_list):
    matches = 0
    matches1 = 0
    for idx, labels in enumerate(predicted_labels_list):
        if not labels: continue
        row_match = 0
        actual_labels = test_labels_list[idx]

        if len(labels) < len(actual_labels):
            for label in labels:
                if label in actual_labels: row_match += 1
            matches1 += row_match/len(labels)
        else:
            for actual_label in actual_labels:
                if actual_label in labels: row_match += 1
            matches1 += row_match/len(actual_labels)

        for label in labels:
            if label in actual_labels: 
                matches += 1
                break


    print "Accuracy by one match:", matches/len(predicted_labels_list)
    print "Accuracy by one-to-one matching:", matches1/len(predicted_labels_list)


# F-measure 
def getFmeasure(test_labels_list, predicted_labels_list):
    TP = 0; FN = 0; FP = 0;  # F-measure does not require TN, good for us :)
    for idx, labels in enumerate(predicted_labels_list):
        if not labels: continue
        actual_labels = test_labels_list[idx]

        TP_temp = 0
        for label in labels:
            if label in actual_labels: 
                TP += 1
                TP_temp += 1
            else: FP += 1
        FN += ( len(actual_labels) - TP_temp )

    print "F-measure: ", 2*TP/(2*TP + FP + FN)



# Run the apriori program, read the rules produced, order it and then subsume
def apriori_read_order_subsume( apriori_args, features_list, labels_list ):

    # Write transaction matrix for APRIORI program to read
    with open(APRIORI_INPUT_PATH, "w") as f:
        for frow, lrow in itertools.izip(features_list, labels_list):
            f.write(' '.join(map(str,frow)) + ' ' + ' '.join(map(str,lrow)) + '\n')

    # Invoke apriori program
    print ""
    apriori_command = ['./apriori', '-tr', APRIORI_INPUT_PATH , RULES_PATH ] + apriori_args
    subprocess.call(apriori_command)
    print ""

    rules = readRules(RULES_PATH)
    rules = orderRules(rules)

    subsume_time = -timeit.default_timer()
    subsumed_rules, uncovered_features_list, uncovered_labels_list = subsumeRules(rules, features_list, labels_list)
    subsume_time += timeit.default_timer()
    print "#Rules before subsumption: ", len(rules)
    print "#Rules after subsumption:  ", len(subsumed_rules)
    print "Subsumption time:", str(subsume_time)
    
    return subsumed_rules, uncovered_features_list, uncovered_labels_list



# Return rules learned from train_set
def train_phase(train_set, apriori_args):
    train_features_list, train_labels_list = separateFeaturesAndLabels(train_set)
    subsumed_rules = []
    uncovered_features_list = train_features_list
    uncovered_labels_list = train_labels_list
    iteration = 0; prev_len = 0
    while len(uncovered_features_list) > 100 and len(uncovered_features_list)!= prev_len and iteration < TOTAL_ITERATIONS:
        iteration += 1; prev_len = len(uncovered_features_list)
        subsumed_rules_temp, uncovered_features_list, uncovered_labels_list = \
        apriori_read_order_subsume( apriori_args, uncovered_features_list, uncovered_labels_list )
        subsumed_rules += subsumed_rules_temp
        print "Dataset uncovered:", len(uncovered_features_list)

    labels = set()
    for rule in subsumed_rules: labels.add(rule[0])
    print "\nNo of labels after", iteration, "iterations:", len(labels)

    return subsumed_rules



def test_phase(test_set, subsumed_rules_clusters, cluster_tms):
    cluster_means = []
    for cluster_tm in cluster_tms:
        tm, labels_list = separateFeaturesAndLabels(cluster_tm)
        cluster_means.append( cc.get_representative_means(tm) )

    test_features_list, test_labels_list = separateFeaturesAndLabels(test_set)
    test_features_clusters, test_labels_clusters = cc.cluster_test_set(test_features_list, test_labels_list, cluster_means)

    for idx in range(len(test_features_clusters)):
        test_features_list = test_features_clusters[idx]
        test_labels_list = test_labels_clusters[idx]
        subsumed_rules = subsumed_rules_clusters[idx]

        print "\nCluster Index:", idx
        predicted_labels_list = testRules(subsumed_rules, test_features_list)
        getAccuracy(test_labels_list, predicted_labels_list)
        getFmeasure(test_labels_list, predicted_labels_list)

        predicted_labels_list = testRulesWithVariableK(subsumed_rules, test_features_list, test_labels_list)
        getAccuracy(test_labels_list, predicted_labels_list)
        getFmeasure(test_labels_list, predicted_labels_list)

    print ""



def main(argv):
    if len(argv) < 4:
        print "Usage: <train-file> <test-file> <cluster-file>"
        print "       OR"
        print "       <train-file> <test-file> <cluster-file> <support-arg> <confidence-arg>"
        sys.exit()

    train_path, test_path, cipath = argv[1: 4]
    if len(argv)>4: apriori_args = argv[4:6]
    else: apriori_args = [ "-s3m3", "-c80" ]

     
    start_time = timeit.default_timer()
    whole_train_set = readDataset(train_path) 
    test_set = readDataset(test_path) 
    cluster_tms = create_cluster_tms(train_path, cipath)
    print "Train size:", len(whole_train_set), "| Test Size:", len(test_set)


    start_time = timeit.default_timer()
    subsumed_rules_clusters = []                                    # Train
    for idx, train_set in enumerate(cluster_tms):                   #
        subsumed_rules = train_phase(train_set, apriori_args)       #
        subsumed_rules_clusters.append(subsumed_rules)              #
    end_time = timeit.default_timer()
    print "Training Time:", str(end_time - start_time), "\n"

    start_time = timeit.default_timer()
    test_phase(test_set, subsumed_rules_clusters, cluster_tms)      # Test
    end_time = timeit.default_timer()
    print "Testing Time:", str(end_time - start_time), "\n"

    end_time = timeit.default_timer()
    print "Total Execution Time:", str(end_time - start_time)



if __name__=="__main__": main(sys.argv)
