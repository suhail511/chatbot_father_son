
import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
import nltk

def cleanMessage(message):
	# Remove new lines within message
	cleanedMessage = message.replace('\n',' ').lower()
	# Remove punctuation
	cleanedMessage = re.sub('([.,!?])','', cleanedMessage)
	# cleanedMessage = re.sub("\\'",'', cleanedMessage)
	# cleanedMessage = re.sub("\\,:",'', cleanedMessage)
	# Remove multiple spaces in message
	cleanedMessage = re.sub(' +',' ', cleanedMessage)
	# cleanedMessage = re.sub('\W+',' ', cleanedMessage)
	return cleanedMessage

#Read file and Remove empty lines
cnvFile = open('files/conversation.txt', 'r')
allLines = cnvFile.readlines()
while '\n' in allLines: allLines.remove('\n')

#convert to everything to lowercase
[x.lower() for x in allLines]

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

np.save('data/fatherConversationDictionary.npy', responseDictionary)

conversationFile = open('data/fatherConversationData.txt', 'w')
for key,value in responseDictionary.items():
    if (not key.strip() or not value.strip()):
        # If there are empty strings
        continue
    conversationFile.write(key.strip() + ' ' + value.strip() +' ')
