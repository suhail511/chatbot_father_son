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

sonsResponse = son.response("Where are you?")
print("Son :" , sonsResponse)
for i in range(10):
    fathersResponse = father.response(sonsResponse)
    print("Father :" , fathersResponse)
    sonsResponse = son.response(fathersResponse)
    print("Son :" , sonsResponse)
