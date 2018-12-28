
# coding: utf-8

# In[1]:


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
import sklearn.manifold
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:



def cleanMessage(corpus_raw):
    corpus_raw = re.sub(r'\n+','.', corpus_raw)
    corpus_raw = re.sub(r'\.+', ". ", corpus_raw)
    corpus_raw = re.sub(r'…', " … ", corpus_raw)
    corpus_raw = re.sub(r'’', "", corpus_raw)
    corpus_raw = corpus_raw.replace("'", "")
    corpus_raw = re.sub(r' +', " ", corpus_raw)
    corpus_raw = re.sub(" +"," ", corpus_raw)
    return corpus_raw


# In[7]:


#Read files
conv_filename = sorted(glob.glob('files/*.txt'))
print("Found files: ", conv_filename)

sonResponseDictionary = dict()
for conv_filename in conv_filename:
    print("Reading '{0}'...".format(conv_filename))
    with codecs.open(conv_filename, "r", "utf-8") as conv_file:
        allLines = conv_file.readlines()
        while '\n' in allLines: allLines.remove('\n')
        #convert to everything to lowercase
        [x.lower() for x in allLines]

        # FOR SON
        personName = "son"

        myMessage, otherPersonsMessage, currentSpeaker = "","",""
        for index,lines in enumerate(allLines):
            justMessage = lines
            colon = justMessage.find(':')
            # Find messages of the current person
            if (justMessage[:colon] == personName):
                if not myMessage:
                    startMessageIndex = index - 1
                myMessage += justMessage[colon+1:]
                if index == 1:
                    prevMessage = allLines[0]
                    colon = prevMessage.find(':')
                    otherPersonsMessage = prevMessage[colon+1:]
                    otherPersonsMessage = cleanMessage(otherPersonsMessage)
                    myMessage = cleanMessage(myMessage)
                    sonResponseDictionary[otherPersonsMessage] = myMessage

            elif myMessage:
                # Now go and see what message the other person sent by looking at previous messages
                for counter in range(startMessageIndex, -1, -1):
                    currentLine = allLines[counter]
                    justMessage = currentLine
                    colon = justMessage.find(':')
                    if not currentSpeaker:
                        # Other speaker
                        currentSpeaker = justMessage[:colon]
                    elif (currentSpeaker != justMessage[:colon] and otherPersonsMessage):
                        # A different person started speaking, so now I know that the first person's message is done
                        otherPersonsMessage = cleanMessage(otherPersonsMessage)
                        myMessage = cleanMessage(myMessage)
                        sonResponseDictionary[otherPersonsMessage] = myMessage
                        break
                    otherPersonsMessage = justMessage[colon+1:] + otherPersonsMessage
                myMessage, otherPersonsMessage, currentSpeaker = "","",""
        if myMessage:
            for counter in range(startMessageIndex, -1, -1):
                    currentLine = allLines[counter]
                    justMessage = currentLine
                    colon = justMessage.find(':')
                    if not currentSpeaker:
                        # Other speaker
                        currentSpeaker = justMessage[:colon]
                    elif (currentSpeaker != justMessage[:colon] and otherPersonsMessage):
                        # A different person started speaking, so now I know that the first person's message is done
                        otherPersonsMessage = cleanMessage(otherPersonsMessage)
                        myMessage = cleanMessage(myMessage)
                        sonResponseDictionary[otherPersonsMessage] = myMessage
                        break
                    otherPersonsMessage = justMessage[colon+1:] + otherPersonsMessage


np.save('data/sonConversationDictionary.npy', sonResponseDictionary)

conversationFile = open('data/sonConversationData.txt', 'w')
for key,value in sonResponseDictionary.items():
    if (not key.strip() or not value.strip()):
        # If there are empty strings
        continue
    conversationFile.write(key.strip() + ' ' + value.strip() + ' ')

print("Created Conversation Dictionary for SON. Size : ", len(sonResponseDictionary))


#Read files
conv_filename = sorted(glob.glob('files/*.txt'))
# print("Found files: ", conv_filename)

fatherResponseDictionary = dict()
for conv_filename in conv_filename:
#     print("Reading '{0}'...".format(conv_filename))
    with codecs.open(conv_filename, "r", "utf-8") as conv_file:
        allLines = conv_file.readlines()
        while '\n' in allLines: allLines.remove('\n')
        #convert to everything to lowercase
        [x.lower() for x in allLines]

        # FOR FATHER
        personName = "father"

        myMessage, otherPersonsMessage, currentSpeaker = "","",""
        for index,lines in enumerate(allLines):
            justMessage = lines
            colon = justMessage.find(':')
            # Find messages of the current person
            if (justMessage[:colon] == personName):
                if not myMessage:
                    startMessageIndex = index - 1
                myMessage += justMessage[colon+1:]
                if index == 1:
                    prevMessage = allLines[0]
                    colon = prevMessage.find(':')
                    otherPersonsMessage = prevMessage[colon+1:]
                    otherPersonsMessage = cleanMessage(otherPersonsMessage)
                    myMessage = cleanMessage(myMessage)
                    fatherResponseDictionary[otherPersonsMessage] = myMessage

            elif myMessage:
                # Now go and see what message the other person sent by looking at previous messages
                for counter in range(startMessageIndex, -1, -1):
                    currentLine = allLines[counter]
                    justMessage = currentLine
                    colon = justMessage.find(':')
                    if not currentSpeaker:
                        # Other speaker
                        currentSpeaker = justMessage[:colon]
                    elif (currentSpeaker != justMessage[:colon] and otherPersonsMessage):
                        # A different person started speaking, so now I know that the first person's message is done
                        otherPersonsMessage = cleanMessage(otherPersonsMessage)
                        myMessage = cleanMessage(myMessage)
                        fatherResponseDictionary[otherPersonsMessage] = myMessage
                        break
                    otherPersonsMessage = justMessage[colon+1:] + otherPersonsMessage
                myMessage, otherPersonsMessage, currentSpeaker = "","",""
        if myMessage:
            for counter in range(startMessageIndex, -1, -1):
                    currentLine = allLines[counter]
                    justMessage = currentLine
                    colon = justMessage.find(':')
                    if not currentSpeaker:
                        # Other speaker
                        currentSpeaker = justMessage[:colon]
                    elif (currentSpeaker != justMessage[:colon] and otherPersonsMessage):
                        # A different person started speaking, so now I know that the first person's message is done
                        otherPersonsMessage = cleanMessage(otherPersonsMessage)
                        myMessage = cleanMessage(myMessage)
                        fatherResponseDictionary[otherPersonsMessage] = myMessage
                        break
                    otherPersonsMessage = justMessage[colon+1:] + otherPersonsMessage


np.save('data/fatherConversationDictionary.npy', fatherResponseDictionary)

conversationFile = open('data/fatherConversationData.txt', 'w')
for key,value in fatherResponseDictionary.items():
    if (not key.strip() or not value.strip()):
        # If there are empty strings
        continue
    conversationFile.write(key.strip() + ' ' + value.strip() + ' ')

print("Created Conversation Dictionary for FATHER. Size : ", len(fatherResponseDictionary))
