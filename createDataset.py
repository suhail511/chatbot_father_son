
import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
import glob
import codecs
from nltk.tokenize import word_tokenize,sent_tokenize

def takeCareOfLongMessages(theDict):

	newresponseDictionary = theDict
	keys = []
	values = []
	for k,v in responseDictionary.items():
	    keys.append(k)
	    values.append(v)

	for index,key in enumerate(keys):
		if len(word_tokenize(key)) >= 50 or len(word_tokenize(values[index])) >= 50 :
			key_sentences = sent_tokenize(key)
			value_sentences = sent_tokenize(values[index])

			for number, value_sentence in enumerate(value_sentences):
				for key_sentence in key_sentences:
					for i in range(number):
						key_sentence += ' <pad> '
					newresponseDictionary[key_sentence] = value_sentence
	return newresponseDictionary
def cleanMessage(message):
	# Remove new lines within message
	cleanedMessage = message.replace('\n',' ').lower()
	# Remove punctuation
	cleanedMessage = re.sub('([.,!?])','', cleanedMessage)
	# Remove multiple spaces in message
	cleanedMessage = re.sub(' +',' ', cleanedMessage)
	cleanedMessage = re.sub('…',' ', cleanedMessage)
	return cleanedMessage

#Read files and Remove empty lines
filenames = sorted(glob.glob('files/*.txt'))
print("Files found: ", filenames)

allLines = []
for filename in filenames:
	with codecs.open(filename, "r", "utf-8") as file:
		allLines.append(file.readlines())
allLines = [item for sublist in allLines for item in sublist]
while '\n' in allLines: allLines.remove('\n')

#This is for the son
personName = 'son'

responseDictionary = dict()
myMessage, otherPersonsMessage, currentSpeaker = "","",""
for index,lines in enumerate(allLines):
    justMessage = lines
    colon = justMessage.find(':')
    # Find messages of the current person
    if (justMessage[:colon] == personName):
        if not myMessage:
            # Want to find the first message that person send (if sent multiple in a row)
            startMessageIndex = index - 1
        myMessage += justMessage[colon+1:]

    elif myMessage:
        # Now go and see what message the other person sent by looking at previous messages
        for counter in range(startMessageIndex, 0, -1):
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
                responseDictionary[otherPersonsMessage] = myMessage
                break
            otherPersonsMessage = justMessage[colon+1:] + otherPersonsMessage
        if startMessageIndex < 1:
            justMessage = lines
            colon = justMessage.find(':')
            otherPersonsMessage = justMessage[colon+1:]
            otherPersonsMessage = cleanMessage(otherPersonsMessage)
            currentLine = allLines[2]
            colon = currentLine.find(':')
            myMessage = cleanMessage(currentLine[colon+1:])
            responseDictionary[otherPersonsMessage] = myMessage
        myMessage, otherPersonsMessage, currentSpeaker = "","",""

responseDictionary = takeCareOfLongMessages(responseDictionary)

np.save('data/sonConversationDictionary.npy', responseDictionary)

conversationFile = open('data/sonConversationData.txt', 'w')
for key,value in responseDictionary.items():
    if (not key.strip() or not value.strip()):
        # If there are empty strings
        continue
    conversationFile.write(key.strip() + ' ' + value.strip() + ' ')


#This is for the Father
personName = 'father'

responseDictionary = dict()
myMessage, otherPersonsMessage, currentSpeaker = "","",""
for index,lines in enumerate(allLines):
    justMessage = lines
    colon = justMessage.find(':')
    # Find messages of the current person
    if (justMessage[:colon] == personName):
        if not myMessage:
            # Want to find the first message that person send (if sent multiple in a row)
            startMessageIndex = index - 1
        myMessage += justMessage[colon+1:]

    elif myMessage:
        # Now go and see what message the other person sent by looking at previous messages
        for counter in range(startMessageIndex, 0, -1):
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
                responseDictionary[otherPersonsMessage] = myMessage
                break
            otherPersonsMessage = justMessage[colon+1:] + otherPersonsMessage
        if startMessageIndex < 1:
            justMessage = allLines[0]
            colon = justMessage.find(':')
            otherPersonsMessage = justMessage[colon+1:]
            otherPersonsMessage = cleanMessage(otherPersonsMessage)
            currentLine = allLines[1]
            colon = currentLine.find(':')
            myMessage = cleanMessage(currentLine[colon+1:])
            responseDictionary[otherPersonsMessage] = myMessage
        myMessage, otherPersonsMessage, currentSpeaker = "","",""

responseDictionary = takeCareOfLongMessages(responseDictionary)

np.save('data/fatherConversationDictionary.npy', responseDictionary)

conversationFile = open('data/fatherConversationData.txt', 'w')
for key,value in responseDictionary.items():
    if (not key.strip() or not value.strip()):
        # If there are empty strings
        continue
    conversationFile.write(key.strip() + ' ' + value.strip() +' ')
