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


df = pd.read_csv(path + filename)

# Functions
def summary_stats(x):

	x = x.groupby('order')[features].mean().reset_index(drop = True).T
	x['Total'] = x.mean(axis=1)
	x = x.round(1)

	return x

def lasso_reg(df, alpha):

	X = df[features]
	y = df['receptiveness']
 
	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.33, random_state=42)
	reg = Lasso(alpha = alpha)
	reg.fit(X_train, y_train)

	pred = reg.predict(X_test)
	r2 = round(r2_score(y_test, pred),2)

	avp_df = pd.DataFrame(data = zip(pred, y_test), columns = ['Pred', 'Actual'])
	avp_df = avp_df.sort_values(by = 'Actual', ascending = True)

	ch.AvP(avp_df['Pred'], avp_df['Actual'], r2, alpha)

	out = pd.DataFrame(list(np.around(np.array(reg.coef_),2)), index = list(X_test), columns = ['coeffs'])

	return out

def analysis(x, alpha):

	res = lasso_reg(x, alpha)
	res = res.sort_values(by = 'coeffs', ascending = False)
	res = res[:5]

	return res
	

def corr_analysis(cond, lag = 0):
# Correlation analysis

	corr_mat = []

	for i in range(3):
		
		# DVs and IVs

		y = df['receptiveness'][(df['order'] == i + 1 + lag) & (df['cond'] == cond)]
		X = df[features][(df['order'] == i + 1 + lag) & (df['cond'] == cond)]

		corr_ls = []
		for j in range(len(list(X))):
			corr, _ = spearmanr(y, X.iloc[:, j])
			corr_ls.append(round(corr, 2))

		corr_mat.append(corr_ls)

	corr_res = pd.DataFrame({
		'Round 1': corr_mat[0],
		'Round 2': corr_mat[1],
		'Round 3': corr_mat[2]
		}, index = list(X))


	corr_res = corr_res.fillna(0)
	corr_res['Average correlation'] = round(corr_res.mean(axis=1),2)
	corr_res = corr_res.sort_values(by = 'Average correlation', ascending = False)

	corr_res['1 to 2'] = corr_res['Round 2'] - corr_res['Round 1']
	corr_res['2 to 3'] = corr_res['Round 3'] - corr_res['Round 2']

	return corr_res

# corr_control = corr_analysis(cond = 'start')
# corr_test = corr_analysis(cond = 'middle')

# print(corr_test)

# find average changes in receptiveness

def recep_decay(df):
	# average decline by round

	cond = ['start', 'middle']
	start_round = [1,2]

	x = df[['ResponseId', 'order', 'cond', 'receptiveness']].set_index('ResponseId')

	diffs = []
	conds = []

	for c in cond:

		for s in start_round:

			x1 = x['receptiveness'][(x['order'] == s) & (x['cond'] == c)]
			x2 = x['receptiveness'][(x['order'] == s + 1) & (x['cond'] == c)]

			diff = (x2 / x1) - 1
			ave_diff = diff.mean()

			diffs.append(ave_diff)
			conds.append(c)

	return pd.DataFrame({'Ave diff': diffs}, index = conds)


# receptiveness_decay = recep_decay(df)
# print(receptiveness_decay)


def index_check(ind1, ind2):

	if ind1.index.tolist() != ind2.index.tolist():
		return 'Check that indicies in both dataframes are the same'
	else:
		return ''

def get_deltas(x, s, c):

	x1 = x[features][(x['order'] == s) & (x['cond'] == c)]
	x2 = x[features][(x['order'] == s + 1) & (x['cond'] == c)]

	print(index_check(x1, x2))

	y1 = x['receptiveness'][(x['order'] == s) & (x['cond'] == c)]
	y2 = x['receptiveness'][(x['order'] == s + 1) & (x['cond'] == c)]

	print(index_check(y1, y2))

	diff_x = (x2 / x1) - 1
	diff_x = diff_x.fillna(0).replace(np.inf, 0)

	ave_x = round((x1.mean() + x2.mean()) / 2, 3)

	diff_y = (y2 / y1) - 1
	diff_y = diff_y.fillna(0).replace(np.inf, 0)

	return diff_y, diff_x, ave_x

def ols_reg(diff_y, diff_x):

	diff_x = sm.add_constant(diff_x, prepend=False)

	mod = sm.OLS(diff_y, diff_x)
	return mod.fit()


def effect_byround(df):
	'''
	Estimate the driver of change between receptiveness and feature counts using OLS regression

	Input:
		Feature counts
		Receptiveness scores
		ResponseID
		Conditions
		Order

	Returns:
		Average feature counts
		Average changes in receptiveness scores and features by round
		Coeff estimate for each change in feature counts against change in receptiveness
		Statistics including p-values and standard errors associated with each coefficient
		R2 return as seperate list
	'''

	cond = ['start', 'middle']
	start_round = [1,2]

	x = df.set_index('ResponseId')

	diffs = []
	conds = []
	r2 = []
	outputs = pd.DataFrame()

	#features.remove('First.Person.Single')

	for c in cond:

		for s in start_round:

			diff_y, diff_x, ave_x = get_deltas(x, s, c)

			res = ols_reg(diff_y, diff_x)

			ave_diff_y = round(diff_y.mean(), 4)
			ave_diff_x = diff_x.mean()

			#print(diff_x.mean())

			output = pd.concat([ave_x, ave_diff_x, res.params, res.bse, res.tvalues, res.pvalues], axis = 1)

			head_text = c + "_" + str(s + 1) + "-" + str(s)
			output.columns = ['Average feature counts','Change in feature counts','coeffs' , 'std err','t-values', 'p-values']

			output = output.sort_values(['p-values', 'coeffs'],
			 ascending = [True, False])
			output = round(output, 2)

			output.insert(0, 'Change in Receptiveness', ave_diff_y)
			output.insert(0, 'Model (cond & order)', head_text)


			if c == 'start' and s == 1:
				outputs = output
			else:
				#outputs = outputs.merge(output, left_index = True, right_index = True)
				outputs = pd.concat([outputs, output], axis = 0)
			r2.append(round(res.rsquared, 2))

	return outputs, r2


#outputs, r2 = effect_byround(df)
#outputs.to_excel('../Out/Outputs_test.xlsx')
#print(outputs)

#print(r2)

#print(list(df))

def features_new():

	# New algorithm test

	UPLOAD_FOLDER	 = '../Data/In/'
	FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_noneg',  'spacy_neg_only', 'word_start', 'spacy_tokentag']

	kw = prep.load_saved_data(UPLOAD_FOLDER, FOLDERS_IN)

	for i in range(len(df['response'])):
		text = df['response'][i]

		scores = fe.feat_counts(text, kw).set_index('Features')
		#print(scores)

		if i == 0:
			res = scores.T
		else:
			res = res.append(scores.T)

	res = res.fillna(0)

	res.to_excel("../Out/feat_new.xlsx")
	return res





def features_old(df, features):

	features.extend(['Token_count'])
	df1 = df[features]
	colnames = list(df1)
	colnames = [names.replace('.','_') for names in colnames]
	df1.columns = colnames

	return df1


def correl_feats(df, features):

	feat_old = features_old(df, features)
	#feat_old.to_excel("../Out/feat_old.xlsx", index = False)
	feat_new = features_new()
	feat_new.to_excel("../Out/feat_new.xlsx", index = False)

	corr_ls = []
	for i in list(feat_old):
		corr, _ = spearmanr(feat_old[i], feat_new[i])
		corr_ls.append(round(corr, 2))

	res = pd.DataFrame({
		'Feature': list(feat_old),
		'Spearman': corr_ls
		})

	return res

# For creating histograms later, drop the conditions where Ps were not exposed to recipe

# indexNames = df[(df['cond'] == 'middle') & (df['order'].isin([1,2]))].index
# df.drop(indexNames, inplace=True)
# df = df.reset_index()
# print(df.head())
# feat_new = features_new()

# res = correl_feats(df, features)
# res_small = res[res['Spearman'] < 0.9]
# res_small.to_excel("../Out/res_small_cleantext.xlsx", index = False)
# res.to_excel("../Out/res_correl_coeffs.xlsx", index = False)

# Plot correlations of where correlation was below 0.9

# df_old = pd.read_excel('../Out/feat_old.xlsx')
df_new = pd.read_excel('../Out/feat_new.xlsx')
# corr = pd.read_excel('../Out/res_correl_coeffs.xlsx')

# low_cc = corr['Feature'][corr['Spearman'] < 0.9]
# print(corr)

def feat_dist(df, x_lab, y_lab, facecolor, color, fontsize):

	
	fig, ax = plt.subplots(3, 3, figsize=(9, 10))
	fig.suptitle('Distribution of key linguistic features')
		
	# fig.subplots_adjust(top=0.7) 

	# the histogram of the data

	feature_name = 'Acknowledgement'
	x1 = df[feature_name]
	ax[0,0].hist(x1, facecolor=facecolor, bins = range(min(x1), max(x1) + 1, 1), rwidth=0.9, align = 'left')
	#ax[0,0].set_xticks(range(min(x1) , max(x1) + 1, 1))
	ax[0,0].axvline(int(x1.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[0,0].set(xticks = range(min(x1), max(x1) + 1, 1), xlim=[- 1, max(x1)])
	ax[0,0].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[0,0].set_xlabel(x_lab, fontsize = fontsize)
	ax[0,0].set_ylabel(y_lab, fontsize = fontsize)
	ax[0,0].tick_params(labelsize= fontsize)
	ax[0,0].patch.set_facecolor('whitesmoke')


	feature_name = 'Agreement'
	x2 = df[feature_name]
	ax[0,1].hist(x2, facecolor=facecolor, bins = range(min(x2), max(x2) + 1, 1), rwidth=0.9, align = 'left')
	# ax[0,1].set_xticks(range(min(x2) , max(x2) + 1, 1))
	ax[0,1].axvline(int(x2.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[0,1].set(xticks = range(min(x2), max(x2) + 1, 1), xlim=[- 1, max(x2)])
	ax[0,1].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[0,1].set_xlabel(x_lab, fontsize = fontsize)
	ax[0,1].set_ylabel(y_lab, fontsize = fontsize)
	ax[0,1].tick_params(labelsize= fontsize)
	ax[0,1].patch.set_facecolor('whitesmoke')

	feature_name = 'Hedges'
	x3 = df[feature_name]
	ax[0,2].hist(x3, facecolor=facecolor, bins = range(min(x3), max(x3) + 1, 1), rwidth=0.9, align = 'left')
	# ax[0,2].set_xticks(range(min(x3) , max(x3) + 1, 1))
	ax[0,2].axvline(int(x3.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[0,2].set(xticks = range(min(x3), max(x3) + 1, 1), xlim=[- 1, max(x3)])
	ax[0,2].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[0,2].set_xlabel(x_lab, fontsize = fontsize)
	ax[0,2].set_ylabel(y_lab, fontsize = fontsize)
	ax[0,2].tick_params(labelsize= fontsize)
	ax[0,2].patch.set_facecolor('whitesmoke')

	feature_name = 'Negation'
	x4 = df[feature_name]
	ax[1,0].hist(x4, facecolor=facecolor, bins = range(min(x4), max(x4) + 1, 1), rwidth=0.9, align = 'left')
	# ax[1,0].set_xticks(range(min(x4) , max(x4) + 1, 1))
	ax[1,0].axvline(int(x4.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[1,0].set(xticks = range(min(x4), max(x4) + 1, 1), xlim=[- 1, max(x4)])
	ax[1,0].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[1,0].set_xlabel(x_lab, fontsize = fontsize)
	ax[1,0].set_ylabel(y_lab, fontsize = fontsize)
	ax[1,0].tick_params(labelsize= fontsize)
	ax[1,0].patch.set_facecolor('whitesmoke')

	feature_name = 'Positive_Emotion'
	x5 = df[feature_name]
	ax[1,1].hist(x5, facecolor=facecolor, bins = range(min(x5), max(x5) + 1, 1), rwidth=0.9, align = 'left')
	# ax[1,1].set_xticks(range(min(x5) , max(x5) + 1, 1))
	ax[1,1].axvline(int(x5.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[1,1].set(xticks = range(min(x5), max(x5) + 1, 1), xlim=[- 1, max(x5)])
	ax[1,1].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[1,1].set_xlabel(x_lab, fontsize = fontsize)
	ax[1,1].set_ylabel(y_lab, fontsize = fontsize)
	ax[1,1].tick_params(labelsize= fontsize)
	ax[1,1].patch.set_facecolor('whitesmoke')

	feature_name = 'Reasoning'
	x6 = df[feature_name]
	ax[1,2].hist(x6, facecolor=facecolor, bins = range(min(x6), max(x6) + 1, 1), rwidth=0.9, align = 'left')
	# ax[1,2].set_xticks(range(min(x6) , max(x6) + 1, 1))
	ax[1,2].axvline(int(x6.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[1,2].set(xticks = range(min(x6), max(x6) + 1, 1), xlim=[- 1, max(x6)])
	ax[1,2].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[1,2].set_xlabel(x_lab, fontsize = fontsize)
	ax[1,2].set_ylabel(y_lab, fontsize = fontsize)
	ax[1,2].tick_params(labelsize= fontsize)
	ax[1,2].patch.set_facecolor('whitesmoke')

	feature_name = 'Subjectivity'
	x7 = df[feature_name]
	ax[2,0].hist(x7, facecolor=facecolor, bins = range(min(x7), max(x7) + 1, 1), rwidth=0.9, align = 'left')
	# ax[2,0].set_xticks(range(min(x7) , max(x7) + 1, 1))
	ax[2,0].axvline(int(x7.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[2,0].set(xticks = range(min(x7), max(x7) + 1, 1), xlim=[- 1, max(x7)])
	ax[2,0].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[2,0].set_xlabel(x_lab, fontsize = fontsize)
	ax[2,0].set_ylabel(y_lab, fontsize = fontsize)
	ax[2,0].tick_params(labelsize= fontsize)
	ax[2,0].patch.set_facecolor('whitesmoke')

	feature_name = 'Adverb_Limiter'
	x8 = df[feature_name]
	ax[2,1].hist(x8, facecolor=facecolor, bins = range(min(x8), max(x8) + 1, 1), rwidth=0.9, align = 'left')
	# ax[2,1].set_xticks(range(min(x8) , max(x8) + 1, 1))
	ax[2,1].axvline(int(x8.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[2,1].set(xticks = range(min(x8), max(x8) + 1, 1), xlim=[- 1, max(x8)])
	ax[2,1].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[2,1].set_xlabel(x_lab, fontsize = fontsize)
	ax[2,1].set_ylabel(y_lab, fontsize = fontsize)
	ax[2,1].tick_params(labelsize= fontsize)
	ax[2,1].patch.set_facecolor('whitesmoke')

	feature_name = 'Second_Person'
	x9 = df[feature_name]
	ax[2,2].hist(x9, facecolor=facecolor, bins = range(min(x9), max(x9) + 1, 1), rwidth=0.9, align = 'left')
	# ax[2,2].set_xticks(range(min(x9) , max(x9) + 1, 1))
	ax[2,2].axvline(int(x9.quantile([0.67])), color=color, linestyle='dashed', linewidth=1)
	ax[2,2].set(xticks = range(min(x9), max(x9) + 1, 1), xlim=[- 1, max(x9)])
	ax[2,2].set_title(feature_name +  '\n two-thirds threshold: '
		+ str(int(list(df[feature_name].quantile([0.67]))[0])), size = 12)
	ax[2,2].set_xlabel(x_lab, fontsize = fontsize)
	ax[2,2].set_ylabel(y_lab, fontsize = fontsize)
	ax[2,2].tick_params(labelsize= fontsize)
	ax[2,2].patch.set_facecolor('whitesmoke')


	fig.subplots_adjust(wspace=0.5)
	fig.subplots_adjust(hspace=0.7)
	# plt.show()
	fig.savefig('../Out/Images/All_hist.png', dpi = 300)

#print(list(df_new))
main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity', 'Adverb_Limiter', 'Second_Person']

feat_dist(df_new, 'Feature counts', 'Count of responses', 'darkblue', 'darkmagenta', 10)
# for i in main_features:
# 	feat_dist(df_new, i)



# df = df_new
# q = pd.DataFrame(df['Subjectivity'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]))
# print(list(q.index))
# print(list(q['Subjectivity']))
# print(list(df['Negation'].quantile([0.67]))[0])



# Exploratory

#print(df.columns)

# Numbers of rows = 1386
#print(df.shape)

# Number of unique ResponseIDs = 462. All respondents gave answers to all rounds
#print(df['ResponseId'].nunique())
#print(df['ResponseId'][df['order'] == 3].nunique())

# Analyse regression

#res = analysis(df, alpha = 0.1)
# res = analysis(df[df['order'] == 3], alpha = 0.1)
#ch.summary_bar(res.index.values.tolist(), res['coeffs'], 'Coeffs', '')


# Create bar plots

#x = df[df['order'] == 3]
#x = df

#x = summary_stats(x).sort_values(by = 'Total', ascending=False)[:10]
#ch.summary_bar(x.index.values.tolist(), x['Total'], 'Feature counts', 'Feature count per document')