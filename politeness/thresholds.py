import os
import pandas as pd
import numpy as np
import charts as ch
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from scipy.stats import spearmanr
import statsmodels.api as sm

import prep
import feature_extraction as fe

# Global Variables
path = '../Data/'
filename = 'features.csv'

features = ['Hedges', 'Positive.Emotion', 'Negative.Emotion', 'Impersonal.Pronoun',
            'Swearing', 'Negation', 'Filler.Pause', 'Informal.Title',
            'Formal.Title', 'Could.You', 'Can.You', 'By.The.Way', 'Let.Me.Know',
            'Goodbye', 'For.Me', 'For.You', 'Reasoning', 'Reassurance', 'Ask.Agency',
            'Give.Agency', 'Hello', 'Please', 'First.Person.Plural', 'First.Person.Single',
            'Second.Person', 'Agreement', 'Acknowledgement', 'Subjectivity', 'Bare.Command',
            'WH.Questions', 'YesNo.Questions', 'Gratitude', 'Apology', 'Truth.Intensifier',
            'Affirmation', 'Adverb.Limiter', 'Conjunction.Start']


main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Subjectivity', 'Adverb_Limiter', 'Disagreement', 'Negative_Emotion']
#thresholds = [0, 1, 1, 2, 3, 0, 1, 0, 1]
thresholds = [0.0, 1.1, 1.4, 1.4, 2.9, 0.0, 0.0, 0.0, 2.9]


df = pd.read_csv('../Out/feat_new.csv')

df = df.div(df['Token_count'], axis=0)
df = df * 100


def get_thresholds():

    thresholds = []

    for i in main_features:

        t = list(df[i].quantile([0.5]))[0]
        thresholds.append(round(t, 1))

    return thresholds


print(get_thresholds())


def create_subplot(f, ax, feature_name, df, x_lab, y_lab, facecolor, color, fontsize):
    """
    Creates one subplot of a histogram distribution of feature count with vertical line and title
    """

    x = df[feature_name]

    ax.hist(x, facecolor=facecolor, bins=range(int(min(x)), int(max(x)) + 1, 1), rwidth=0.9, align='left')
    #ax.set_xticks(range(min(x) , max(x) + 1, 1))
    ax.axvline(thresholds[f], color=color, linestyle='dashed', linewidth=1)
    ax.set(xticks=range(int(min(x)), int(max(x)) + 1, 1), xlim=[- 1, max(x)])
    ax.set_title(feature_name + '\nbenchmark: '
                 + str(thresholds[f]), size=12)
    ax.set_xlabel(x_lab, fontsize=fontsize)
    ax.set_ylabel(y_lab, fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    ax.patch.set_facecolor('whitesmoke')


def feat_dist(df, x_lab, y_lab, facecolor, color, fontsize):

    fig = plt.figure(figsize=(9, 10))
    fig.suptitle('Distribution of key linguistic features per 100 words')

    for f in range(len(main_features)):
        ax = fig.add_subplot(3, 3, f + 1)
        create_subplot(f, ax, main_features[f], df, x_lab, y_lab, facecolor, color, fontsize)

    fig.subplots_adjust(wspace=0.5)
    fig.subplots_adjust(hspace=0.7)
    # plt.show()
    fig.savefig('../Out/Images/All_hist2.png', dpi=300)


feat_dist(df, 'Feature counts', 'Count of responses', 'darkgray', 'mediumvioletred', 10)

t = get_thresholds()
print(t)

feat_dist(df, 'Feature counts', 'Count of responses', 'darkgray', 'mediumvioletred', 10)
