import numpy as np
import re
import glob
import codecs
from nltk.tokenize import sent_tokenize,word_tokenize
import pickle

def takeCareOfLongMessages(theDict):

    newresponseDictionary = theDict
    keys = []
    values = []
    for k,v in theDict.items():
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


def addEnfOfMessage(theDict):
    newresponseDictionary = theDict
    keys = []
    values = []
    for k,v in theDict.items():
        v += ' endofmessage '
        newresponseDictionary[k] = v
    return newresponseDictionary

def cleanMessage(message):
    # Remove new lines within message
    cleanedMessage = message.replace('\n','').lower()
    # Remove punctuation
    cleanedMessage = re.sub('\(\[\]\)','', cleanedMessage)
    # Remove multiple spaces in message
    cleanedMessage = re.sub(' +',' ', cleanedMessage)
    cleanedMessage = re.sub('-+','-', cleanedMessage)
    cleanedMessage = re.sub('…',' ', cleanedMessage)
    cleanedMessage = re.sub('\.+','.', cleanedMessage)
    return cleanedMessage

def createResponseDict(name):
    personName = name

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
                    currentSpeaker = justMessage[:colon]
                elif (currentSpeaker != justMessage[:colon] and otherPersonsMessage):
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
    # responseDictionary = addEnfOfMessage(responseDictionary)

    print('Response Dictionaty for {} created'.format(name))
    return responseDictionary

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
responseDictionary = createResponseDict('son')

np.save('data/sonConversationDictionary.npy', responseDictionary)

conversationFile = open('data/sonConversationData.txt', 'w')
for key,value in responseDictionary.items():
    if (not key.strip() or not value.strip()):
        # If there are empty strings
        continue
    conversationFile.write(key.strip() + ' ' + value.strip() + ' ')
conversationFile.close()

#This is for the father
responseDictionary = createResponseDict('father')

np.save('data/fatherConversationDictionary.npy', responseDictionary)

conversationFile = open('data/fatherConversationData.txt', 'w')
for key,value in responseDictionary.items():
    if (not key.strip() or not value.strip()):
        # If there are empty strings
        continue
    conversationFile.write(key.strip() + ' ' + value.strip() + ' ')
conversationFile.close()


## Creating Wordlists
def processDataset(filename):
    openedFile = open(filename, 'r')
    allLines = openedFile.readlines()
    myStr = ""
    for line in allLines:
        myStr += line
    finalDict = list(set(word_tokenize(myStr)))
    return myStr, finalDict

def cleanDict(datasetDictionary):
    if "I." in datasetDictionary: datasetDictionary.remove("i.").remove('c')
    return datasetDictionary

#this is for son-bot
fullCorpus, datasetDictionary = processDataset('data/sonConversationData.txt')
print('Finished parsing and cleaning dataset')

# Remove unwanted words/foul language etc.
datasetDictionary = cleanDict(datasetDictionary)
wordList = list(datasetDictionary)

with open("data/sonWordList.txt", "wb") as fp:
	pickle.dump(wordList, fp)
print('Created file data/sonWordList.txt')

#this is for father-bot
fullCorpus, datasetDictionary = processDataset('data/fatherConversationData.txt')
print('Finished parsing and cleaning dataset')

# Remove unwanted words/foul language etc.
datasetDictionary = cleanDict(datasetDictionary)
wordList = list(datasetDictionary)

with open("data/fatherWordList.txt", "wb") as fp:
	pickle.dump(wordList, fp)
print('Created file data/fatherWordList.txt')
