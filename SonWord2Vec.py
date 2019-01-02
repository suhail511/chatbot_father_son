import tensorflow as tf
import numpy as np
import re
from collections import Counter
import sys
import math
from random import randint
import pickle
import os

# This Word2Vec implementation is largely based on this paper
# https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf
# It's a bit old, but Word2Vec is still SOTA and relatively simple, so I'm going with it

# Check out Tensorflow's documentation which is pretty good for Word2Vec
# https://www.tensorflow.org/tutorials/word2vec

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
