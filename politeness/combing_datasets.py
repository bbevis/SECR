import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

UPLOAD_FOLDER = '../Data/'

import feature_extraction as fe
import prep
import keywords


f1 = 'skillsDatOneraw.csv'
df1 = pd.read_csv(UPLOAD_FOLDER + f1)

# f2 = 'skillsDatTworaw.csv'
# df2 = pd.read_csv(UPLOAD_FOLDER + f2)

keep = ['PROLIFIC_PID', 'cond', 'response1', 'response2', 'response3']

df1 = df1[keep]

