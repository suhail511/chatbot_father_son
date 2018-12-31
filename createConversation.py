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
system_arguments = []
system_arguments = (sys.argv)
if system_arguments == []:
    system_arguments.append(1,"How are you?")
    system_arguments.append(2,10)

# orig_stdout = sys.stdout
# f = open('outputs/out.txt', 'w')
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
