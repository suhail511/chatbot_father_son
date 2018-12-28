import tensorflow as tf
import numpy as np
import sys
from random import randint
import datetime
from sklearn.utils import shuffle
import pickle
import os
import time

# Removes an annoying Tensorflow warning
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def getTestInput(inputMessage, wList, maxLen):
	encoderMessage = np.full((maxLen), wList.index('<pad>'), dtype='int32')
	inputSplit = inputMessage.lower().split()
	for index,word in enumerate(inputSplit):
		if index > maxLen-3:
			break
		try:
			encoderMessage[index] = wList.index(word)
		except ValueError:
			continue
	encoderMessage[index + 1] = wList.index('<EOS>')
	encoderMessage = encoderMessage[::-1]
	encoderMessageList=[]
	for num in encoderMessage:
		encoderMessageList.append([num])
	return encoderMessageList

def idsToSentence(ids, wList):
    EOStokenIndex = wList.index('<EOS>')
    padTokenIndex = wList.index('<pad>')
    myStr = ""
    listOfResponses=[]
    for num in ids:
        if (num[0] == EOStokenIndex or num[0] == padTokenIndex):
            listOfResponses.append(myStr)
            myStr = ""
        else:
            myStr = myStr + wList[num[0]] + " "
    if myStr:
        listOfResponses.append(myStr)
    listOfResponses = [i for i in listOfResponses if i]
    return listOfResponses

# Hyperparamters
batchSize = 24
maxEncoderLength = 15
maxDecoderLength = maxEncoderLength + 1
lstmUnits = 112
embeddingDim = lstmUnits
numLayersLSTM = 3

# Loading in all the data structures
with open("data/SonWordList.txt", "rb") as fp:
	wordList = pickle.load(fp)

vocabSize = len(wordList)

# Need to modify the word list as well
wordList.append('<pad>')
wordList.append('<EOS>')
vocabSize = vocabSize + 2

tf.reset_default_graph()

# Create the placeholders
encoderInputs = [tf.placeholder(tf.int32, shape=(None,)) for i in range(maxEncoderLength)]
decoderLabels = [tf.placeholder(tf.int32, shape=(None,)) for i in range(maxDecoderLength)]
decoderInputs = [tf.placeholder(tf.int32, shape=(None,)) for i in range(maxDecoderLength)]
feedPrevious = tf.placeholder(tf.bool)

encoderLSTM = tf.nn.rnn_cell.LSTMCell(lstmUnits, state_is_tuple=True, name='basic_lstm_cell')


decoderOutputs, decoderFinalState = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(encoderInputs, decoderInputs, encoderLSTM,
															vocabSize, vocabSize, embeddingDim, feed_previous=feedPrevious)

decoderPrediction = tf.argmax(decoderOutputs, 2)

lossWeights = [tf.ones_like(l, dtype=tf.float32) for l in decoderLabels]
loss = tf.contrib.legacy_seq2seq.sequence_loss(decoderOutputs, decoderLabels, lossWeights, vocabSize)
optimizer = tf.train.AdamOptimizer(1e-4).minimize(loss)

sess = tf.Session()
saver = tf.train.Saver()
sess.run(tf.global_variables_initializer())
# Loading in a saved model
if (os.path.isfile('models/son/checkpoint')):
	print('Training Models Found')
	saver.restore(sess, tf.train.latest_checkpoint('models/son/'))

zeroVector = np.zeros((1), dtype='int32')

def response(inputStatement):
	inputVector = getTestInput(inputStatement, wordList, maxEncoderLength);
	feedDict = {encoderInputs[t]: inputVector[t] for t in range(maxEncoderLength)}
	feedDict.update({decoderLabels[t]: zeroVector for t in range(maxDecoderLength)})
	feedDict.update({decoderInputs[t]: zeroVector for t in range(maxDecoderLength)})
	feedDict.update({feedPrevious: True})
	ids = (sess.run(decoderPrediction, feed_dict=feedDict))
	result = idsToSentence(ids, wordList)
	return ''.join(result)
