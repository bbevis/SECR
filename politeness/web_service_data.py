#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 00:56:55 2021

@author: burintbevis
"""
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

print(os.getcwd())

os.chdir('/Users/bb320/BNM Dropbox/Imperial/7_Receptiveness/Analysis/politeness')

file = '../Data/skillsDatOneraw.csv'

df = pd.read_csv(file)

keep = ['ResponseId', 'seedID3', 'issue', 'issue_pos', 'seedtext3','issuetext','cond','response3']

df1 = df[keep]


df1['wd_count'] = df1['response3'].str.split().str.len()

df1 = df1.loc[df1['wd_count'] >= 10]


df1 = df1.dropna()

df1['count'] = 0
df1['ragree'] = np.where(df1['issue_pos'] > 3, 1, 0)

# Create unique key
# df1['ResponseIssueId'] = df1['ResponseId'] + df1['seedID3']


# test
# tmp = df1[df1['ResponseIssueId'] == 'R_3FIH7229XWzTGmyisisPro2']



# remove unnecessary columns
df1 = df1.drop(['wd_count', 'seedID3', 'issue_pos'], axis = 1)

print(list(df1))

cols = [ 'ResponseId', 'issue', 'seedtext', 'issuetext', 'cond', 'rtext', 'count', 'ragree']
df1.columns = cols

# Rearrange columns

cols = ['ResponseId', 'ragree', 'issue', 'issuetext', 'rtext', 'seedtext', 'cond', 'count']
df1 = df1[cols]

# Remove line breaks in excel/csv
import re
df1['rtext'] = df1['rtext'].apply(lambda x: re.sub("\n|\r", "",x))

df1.to_csv('../Out/responses_s1_r3.csv', index = False)

# Counting unique values
df1['cond'].value_counts()

# there are 279 in the middle condition and 262 in the start condition

# random sample to get 100 of each conditions

middle = df1[df1['cond'] == 'middle']
middle = middle.sample(n = 100)


start = df1[df1['cond'] == 'start']

start = start.sample(n = 100)


df2 = pd.concat([middle, start])

df2.to_csv('../Out/responses_s1_r3.csv', index = False)
