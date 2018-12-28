
import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
from collections import Counter
import pickle

import codecs
import glob
import logging
import multiprocessing
import pprint

import nltk
import gensim.models.word2vec as w2v
from gensim.models import Word2Vec
from gensim.models.word2vec import Text8Corpus
import sklearn.manifold
import matplotlib.pyplot as plt
import seaborn as sns

#Read files
conv_filename = sorted(glob.glob('files/*.txt'))
print("Found files: ", conv_filename)

#combine all files in corpus
corpus_raw = u""
for conv_filename in conv_filename:
    print("Reading '{0}'...".format(conv_filename))
    corpus_raw += ' *----------* '
    with codecs.open(conv_filename, "r", "utf-8") as conv_file:
        corpus_raw += conv_file.read()

    print("Corpus is now {0} characters long".format(len(corpus_raw)))
    print()

#turn words into tokens
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

corpus_raw = re.sub(r'\n+','.', corpus_raw)
corpus_raw = re.sub(r'\.+', ". ", corpus_raw)
corpus_raw = re.sub(r'…', " … ", corpus_raw)
corpus_raw = re.sub(r'’', "", corpus_raw)
corpus_raw = re.sub(r"/'", "", corpus_raw)
corpus_raw = re.sub(r' +', " ", corpus_raw)
corpus_raw = re.sub(r'son:','', corpus_raw)
corpus_raw = re.sub(r'father:','', corpus_raw)
corpus_raw = re.sub(" +"," ", corpus_raw)

#convert to everything to lowercase
corpus_raw = corpus_raw.lower()

#convert into a list of words
#remove unnnecessary,, split into words, no hyphens
def sentence_to_wordlist(raw):
    clean = re.sub("/'","", raw)
    clean = re.sub("[^a-zA-Z]"," ", raw)
    words = clean.split()
    return words


def processDataset(allLines):
    myStr = ""
    for line in allLines:
        myStr += line
    myStr = re.sub("[^a-zA-Z]"," ", myStr)
    finalDict = Counter(myStr.split())
    return myStr, finalDict

fullCorpus, datasetDictionary = processDataset(corpus_raw)
print('Finished parsing and cleaning dataset')
wordList = list(datasetDictionary.keys())

with open("data/wordList.txt", "wb") as fp:
	pickle.dump(wordList, fp)
print(len(wordList), 'unique words found')
print('Created file data/wordList.txt')


raw_sentences = tokenizer.tokenize(corpus_raw)
#sentence where each word is tokenized
sentences = []
for raw_sentence in raw_sentences:
    if len(raw_sentence) > 0:
        sentences.append(sentence_to_wordlist(raw_sentence))

# print(raw_sentences[890])
# print(sentence_to_wordlist(raw_sentences[890]))
token_count = sum([len(sentence) for sentence in sentences])
print("The chat corpus contains {0:,} tokens".format(token_count))

raw_sentences = tokenizer.tokenize(corpus_raw)

# Dimensionality of the resulting word vectors.
#more dimensions, more computationally expensive to train
#but also more accurate
#more dimensions = more generalized
num_features = 300
# Minimum word count threshold.
min_word_count = 3

# Number of threads to run in parallel.
#more workers, faster we train
num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 7

# Downsample setting for frequent words.
#0 - 1e-5 is good for this
downsampling = 0

# Seed for the RNG, to make the results reproducible.
#random number generator
#deterministic, good for debugging
seed = 1

chat2vec = w2v.Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=num_features,
    min_count=min_word_count,
    window=context_size,
    sample=downsampling
)

chat2vec.build_vocab(sentences)

print("Word2Vec vocabulary length: ", len(chat2vec.wv.vocab))


chat2vec.train(sentences, total_examples=chat2vec.corpus_count, epochs=10)


np.save('data/embeddingMatrix.npy', chat2vec.wv.vectors)
