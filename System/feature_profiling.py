import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

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
'Affirmation', 'Adverb.Just', 'Conjunction.Start']


df = pd.read_csv(path + filename)

#print(list(df))

cluster_by = ['receptiveness', 'token_count']
X = df[cluster_by]
vars_of_interests = ['Agreement', 'Acknowledgement', 'Positive.Emotion', 'Reasoning', 'Subjectivity', 'Hedges', 'For.Me']


scaler = StandardScaler()
X = scaler.fit_transform(X)

range_n_clusters = [2, 3, 4, 5, 6]

# plt.scatter(X[:,0], X[:,1]) 
# plt.show()
# ss_avg = []

# for n_clusters in range_n_clusters:
# 	kmeans = KMeans(n_clusters=n_clusters)
# 	label = kmeans.fit_predict(X)
# 	ss_avg.append(silhouette_score(X, label))

# print(ss_avg)
# plt.plot(ss_avg)
# plt.show()


kmeans = KMeans(n_clusters=4)
label = kmeans.fit_predict(X)

# Print chart
# u_labels = np.unique(label)

# for i in u_labels:
#     plt.scatter(X[label == i , 0] , X[label == i , 1] , label = i)
# plt.legend()
# plt.show()


def feature_profiles(df, vars_of_interests, label):

	feat_counts_ave = pd.DataFrame()

	for i in range(4):
		x = df[vars_of_interests]
		x1 = x[label == i]
		res = pd.DataFrame(x1.mean())

		if i == 0:
			feat_counts_ave = pd.DataFrame(x1.mean())
		else:
			feat_counts_ave = pd.concat([feat_counts_ave, res], axis = 1)

	feat_counts_ave.columns = ['r_low t_low', 'r_low t_med', 'r_med t_high', 'r_high t_high']
	
	return feat_counts_ave

out = feature_profiles(df, vars_of_interests, label)
print(out)

ax = out.plot.bar(rot=0)
plt.show()


