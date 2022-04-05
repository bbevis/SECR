# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

print(os.chdir('./OneDrive - Imperial College London/7_MRes_project/Analysis/politeness'))

df = pd.read_csv('../Data/sentdat_trim.csv')
df = df[df['sent_count'] == 3]

keep = [
 'sentence_id',
 'Acknowledgement',
 'Agreement',
 'Hedges',
 'Subjectivity',
 'Positive.Emotion',
 'Adverb.Limiter',
 'Reasoning',
 'Negation'
]

var = 'Positive.Emotion'

# Subset data for where we observe feature in sent 1
# get list of doc_ids where sent 1 contains  positive count for feature
feat_exist = df['doc_id'][(df[var] > 0) & (df['sentence_id'] == 1)].tolist()
df_exist = df[df['doc_id'].isin(feat_exist)]
   

df1 = df_exist.loc[:,keep]
df1 = df1.melt(id_vars = 'sentence_id')
df1['Sent 1'] = 'yes'


# Repeat for where feature does not exist in sent 1

df_notexist = df[~df['doc_id'].isin(feat_exist)]
df2 = df_notexist.loc[:,keep]
df2 = df2.melt(id_vars = 'sentence_id')
df2['Sent 1'] = 'no'

# stack dataframes
df3 = pd.concat([df1, df2])


# plot

g = sns.FacetGrid(df3, col='variable',  col_wrap=4, sharey=False)
g.map_dataframe(sns.pointplot, x='sentence_id', y='value', hue = 'Sent 1',
                dodge = True)
g.add_legend()
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle(var)

g.savefig('../Out/Images/cond counts ' + var + '.png')

##### Counting features by sentences
df1 = df.loc[:,keep]
df1 = df1.melt(id_vars = 'sentence_id')

sns.set_style("ticks",{'axes.grid' : True})
g = sns.FacetGrid(df1, col='variable',  col_wrap=4, sharey=False, margin_titles = True)
g.map_dataframe(sns.pointplot, x='sentence_id', y='value',
                dodge = True)
g.add_legend()
g.fig.subplots_adjust(top=0.85)
g.fig.suptitle('Average feature usage by sentence', fontsize=20)
g.axes[0].set_ylabel('Average feature usage', fontsize=14)
g.axes[4].set_ylabel('Average feature usage', fontsize=14)
g.axes[4].set_xlabel('Sentence number', fontsize=14)
g.axes[5].set_xlabel('Sentence number', fontsize=14)
g.axes[6].set_xlabel('Sentence number', fontsize=14)
g.axes[7].set_xlabel('Sentence number', fontsize=14)


g.savefig('../Out/Images/Feature count by sentence.png')


##### Probability of next feature
cp1 = df1[df1['sentence_id'] != 1]
cp1.loc[cp1['value'] > 0, 'value'] = 1

cp1 = cp1.groupby(['variable']).mean()
cp1 = cp1.drop('sentence_id', axis = 1)
cp1['Sent 1'] = 'yes'


cp2 = df2[df2['sentence_id'] != 1]
cp2.loc[cp2['value'] > 0, 'value'] = 1

cp2 = cp2.groupby(['variable']).mean()
cp2 = cp2.drop('sentence_id', axis = 1)
cp2['Sent 1'] = 'no'

cp3 = pd.concat([cp1, cp2], axis = 0)
#cp3.columns = ['Feature in sent 1', 'Feature not in sent 1']


plt.figure(figsize=(10,5))
ax = sns.pointplot(data = cp3, x=cp3.index, y='value', hue = 'Sent 1', 
                   dodge = True).set_title(var)
plt.xticks(rotation = 45)

plt.savefig('../Out/Images/cond prob ' + var + '.png', bbox_inches='tight')




