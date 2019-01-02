import tensorflow as tf
import numpy as np
import re
from collections import Counter
import sys
import math
from random import randint
import pickle
import os


def processDataset(filename):
	openedFile = open(filename, 'r')
	allLines = openedFile.readlines()
	myStr = ""
	for line in allLines:
	    myStr += line
	finalDict = Counter(myStr.split())
	return myStr, finalDict

fullCorpus, datasetDictionary = processDataset('data/sonConversationData.txt')
print('Finished parsing and cleaning dataset')
wordList = list(datasetDictionary.keys())

with open("data/SonWordList.txt", "wb") as fp:
	pickle.dump(wordList, fp)
print('Created file data/SonWordList.txt')
