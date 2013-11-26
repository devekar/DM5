#!/bin/bash

grep "Accuracy" * > accuracy
grep "F-measure" * > fmeasure
grep "Training Time" * > trainingTime
grep "Testing Time" * > testingTime
