# import tensorflow as tf
# import numpy as np
# import sys
# from random import randint
# import datetime
# from sklearn.utils import shuffle
# import pickle
# import os
# import time

import SonResponse as son
import FatherResponse as father
import sys
from random import randint
import time


system_arguments = []
system_arguments = (sys.argv)

# t,s = str(time.time()).split('.')
# filename = t+".txt"
# print ("writing to", filename)


conversationStarters = ["I know",
					"Are you sure?",
					"How are you son?",
					"Remarkable",
					"Did you hear from Law School",
                    "Good morning",
                    "Hey",
                    "Can we have a talk?",
                    "How are you?",
                    "Do you want anything?",
                    "Hi",
                    "Did you find it?",
                    "How were your vacations",
                    "You sister is worried",
                    "Clean the kitchen please"
                    "What song is that?"
					]
num = randint(0,len(conversationStarters) - 1)
if len(system_arguments) <= 1:
    system_arguments.append(conversationStarters[num])
    system_arguments.append(30)
print(system_arguments)
# orig_stdout = sys.stdout
# f = open('outputs/'+filename, 'w')
# sys.stdout = f


print("Father :" , system_arguments[1])
sonsResponse = son.response(system_arguments[1])
print("Son :" , sonsResponse)
for i in range(int(system_arguments[2])):
    fathersResponse = father.response(sonsResponse)
    print("Father :" , fathersResponse)
    sonsResponse = son.response(fathersResponse)
    print("Son :" , sonsResponse)

# sys.stdout = orig_stdout
# f.close()
