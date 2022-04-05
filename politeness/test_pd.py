import os
import numpy as np
import pandas as pd
import feature_extraction as fe
import prep

PATH = '../Data/'
UPLOAD_FOLDER	 = '../Data/In/'
DOWNLOAD_FOLDER	 = '../data/Out/'
FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']
READ_TYPE  = ['single', 'multiple', 'multiple', 'single', 'single', 'single']

main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity', 'Adverb_Limiter', 'Second_Person']
main_features_pos = ['Acknowledgement', 'Agreement', 'Hedges', 'Positive_Emotion', 'Subjectivity', 'Second_Person']
main_features_neg = ['Negation', 'Reasoning', 'Adverb_Limiter']
main_features_old = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive.Emotion', 'Reasoning', 'Subjectivity', 'Adverb.Limiter', 'Second.Person']

thresholds = [0.0, 1.1, 1.4, 1.4, 2.9, 0.0, 0.0, 0.0, 0.0]


kw = prep.load_saved_data(UPLOAD_FOLDER, FOLDERS_IN)


def get_df(cond):

	filename = 'byround.csv'
	df = pd.read_csv(PATH + filename)
	df = df[df['cond'] == cond]

	return df

def normalise_scores(scores):

	"""
	Divides feature counts by 100 words/tokens
	"""

	token_count = list(scores['Counts'][scores['Features'] == 'Token_count'])[0]
	scores['Counts_norm'] = scores['Counts'] / token_count * 100

	return scores


def threshold_df():

	thresh_df = pd.DataFrame({
		'main_features': main_features,
		'thresholds': thresholds
		})

	return thresh_df

def imp_main(df, thresh_df, main_features):

	scores_all = pd.DataFrame()
	feats_ls = []

	for r in range(df.shape[0]):

		scores = fe.feat_counts(df['response'].iloc[r], kw)
		scores = normalise_scores(scores)
		scores = scores.loc[scores['Features'].isin(main_features)]
		scores = pd.merge(scores, thresh_df, left_on = 'Features', right_on = 'main_features')
		scores['diff'] = scores['diff'] = scores['Counts_norm'] - scores['thresholds']

		

		improve_ls = []
		maintain_ls = []

		main_features = scores['main_features'].tolist()
		feats_ls.append(main_features)

		for i in main_features:

			improve = 0
			maintain = 0

			diff = scores['diff'].loc[scores['Features'] == i].to_list()[0]
			if diff <= 0 and i in main_features_pos:
				improve = improve + 1
			elif diff > 0 and i in main_features_pos:
				maintain = maintain + 1
			elif diff > 0 and i in main_features_neg:
				improve = improve + 1
			elif diff <= 0 and i in main_features_neg:
				maintain = maintain + 1

			improve_ls.append(improve)
			maintain_ls.append(maintain)


		scores['improve'] = improve_ls
		scores['maintain'] = maintain_ls
		scores['order'] = df['order'].iloc[r]
		scores['PROLIFIC_PID'] = df['PROLIFIC_PID'].iloc[r]

		scores_all = scores_all.append(scores)

	# print(list(df))
	return scores_all, feats_ls

def add_messages(df, scores,feats_ls):

	messages = []

	for i in range(len(feats_ls)):

		feats_ls1 = feats_ls[i]
		df1 = df.iloc[i]

		for j in range(len(feats_ls1)):
		
			f = feats_ls1[j]
			message = df1[f+'_']
			messages.append(message)

	scores['feedback'] = messages

	return scores

def check_outputs(df, scores):

	
	response = []

	for i in range(scores.shape[0]):

		message = scores['feedback'].iloc[i]

		pos_above = 'used enough'
		pos_below = 'could use more'
		neg_above = 'too many'
		neg_below = 'avoided'

		if pos_above in message:
			response.append('maintain')
		elif pos_below in message:
			response.append('improve')
		elif neg_above in message:
			response.append('improve')
		elif neg_below in message:
			response.append('maintain')

	scores['response type'] = response

	return scores


# df = get_df('feedback')
# thresh_df = threshold_df()
# scores, feats_ls = imp_main(df, thresh_df, main_features)
# scores = add_messages(df, scores, feats_ls)
# scores = check_outputs(df, scores)
# print(scores)

# scores.to_csv('../Out/main_exploratory_analysis.csv', index = False)

df = pd.read_csv('../Out/main_exploratory_analysis.csv')

# D1 = pd.get_dummies(df['Features'])
# df = pd.concat([df, D1], axis = 1)


df = df[df['Features'].isin(['Acknowledgement'])]
# df = df.drop(main_features_neg, axis = 1)


Y = df[['Features', 'PROLIFIC_PID', 'Counts_norm', 'order']][df['order'] == 2]

X_vars = ['Features', 'PROLIFIC_PID', 'order', 'improve']
X = df[X_vars][df['order'] == 1]
X['order'] = X['order'] + 1


df = pd.merge(Y, X, how = 'left', left_on = ['Features', 'PROLIFIC_PID', 'order'],
	right_on = ['Features', 'PROLIFIC_PID', 'order'])


import statsmodels.api as sm
print(list(df))
# df['Counts_norm'] = np.log(df['Counts_norm'])
temp = df['Counts_norm'].isnull().sum()
print(temp)

Y = df['Counts_norm']


X = df.drop(['Counts_norm','Features', 'PROLIFIC_PID', 'order'], axis = 1)

print(Y[:5])

print(X[:5])

X = sm.add_constant(X)
model = sm.OLS(Y,X)
results = model.fit()
print(results.summary())
