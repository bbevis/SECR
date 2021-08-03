import os
import time
import pandas as pd
import re
import prep
import feature_extraction as fe
import responses
import keywords
# import spacy
# import en_core_web_sm
import json
# import requests
import cgi
import cgitb

#--- VARS ---#
PATH = '../Data/'
UPLOAD_FOLDER	 = '../Data/In/'
DOWNLOAD_FOLDER	 = '../data/Out/'
ALLOWED_EXTENSIONS = set(['.txt'])

FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']
READ_TYPE  = ['single', 'multiple', 'multiple', 'single', 'single', 'single']

main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity', 'Adverb_Limiter', 'Second_Person']
main_features_pos = ['Acknowledgement', 'Agreement', 'Hedges', 'Positive_Emotion', 'Subjectivity', 'Second_Person']
main_features_neg = ['Negation', 'Reasoning', 'Adverb_Limiter']
#thresholds = [0, 1, 1, 2, 3, 0, 1, 0, 1]
thresholds = [0.0, 1.1, 1.4, 1.4, 2.9, 0.0, 0.0, 0.0, 0.0]


# nlp = en_core_web_sm.load()

# kw is a dictionary of all key words, dependency pairs and negation words
#kw = prep.load_saved_data(UPLOAD_FOLDER, FOLDERS_IN)
#print(json.dumps(kw,sort_keys=True, indent=4))

kw = keywords.kw
#print(kw)

#--- HELPER FUNCTIONS ---#

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_in():
	if not os.path.exists(UPLOAD_FOLDER):
		os.makedirs(UPLOAD_FOLDER)

def create_out():
	if not os.path.exists(DOWNLOAD_FOLDER):
		os.makedirs(DOWNLOAD_FOLDER)

#--- MAIN FUNCTIONS ---#

def commit_new_data():

	prep.commit_data(PATH, UPLOAD_FOLDER, FOLDERS_IN, READ_TYPE)


def top_bottom_feats(scores):

	"""
	Returns two lists
	1. A list of recognition features where the feature count is > 0
	2. A list of top 3 improvement features where the the feature count
	relative to the threshold is lower
	"""

	scores = scores[scores['Features'].isin(main_features)]
	cutoffs = pd.DataFrame({
		'main_features': main_features,
		'thresholds': thresholds
		})
	scores = pd.merge(scores, cutoffs, left_on = 'Features', right_on='main_features', how = 'left')
	

	scores['diff'] = scores['Counts_norm'] - scores['thresholds']
	scores = scores.sort_values('diff')

	# imp_feats = list(scores['Features'])
	#bottom3 = list(scores['Features'][-3:])

	# recog_feats = scores['Features'][scores['Counts'] > 0]

	# print(imp_feats)

	return scores

def get_main_response(imp_feats):

	"""Returns a list of responses for the improvement features"""

	top_feats = [responses.fancy_responses[imp_feats[i]]['fancy_name'] for i in range(len(imp_feats))]
	top_examples = [responses.fancy_responses[imp_feats[i]]['examples'] for i in range(len(imp_feats))]
	main_response = [a + ' ' + b for a, b in zip(top_feats, top_examples)]

	return main_response

def get_recognition(recog_feats):

	"""
	Returns a list of responses for the recognition features if in recog_feats list
	otherwise returns blank
	"""

	recog_list = recog_feats.to_list()

	bottom_feats = [responses.fancy_responses[i]['fancy_name'] for i in main_features]
	bottom_examples = [responses.fancy_responses[i]['desc'] if i in recog_list else 'were not used' for i in main_features]
	main_response = [a + ' ' + b for a, b in zip(bottom_feats, bottom_examples)]

	return main_response

def get_feedback(scores):

	"""
	Returns a list of responses for the recognition features if in recog_feats list
	otherwise returns a response from the improvment list
	"""

	# feedback = [responses.fancy_responses[i]['recog'] if i in recog_feats else responses.fancy_responses[i]['imp'] for i in main_features]

	feedback = []

	for i in main_features:
		diff = scores['diff'].loc[scores['Features'] == i].to_list()[0]
		if i in main_features_pos and diff <= 0:
			feedback.append(responses.fancy_responses[i]['imp'])
		elif i in main_features_pos and diff > 0:
			feedback.append(responses.fancy_responses[i]['recog'])
		elif i in main_features_neg and diff > 0:
			feedback.append(responses.fancy_responses[i]['recog'])
		elif i in main_features_neg and diff <= 0:
			feedback.append(responses.fancy_responses[i]['imp'])

	return feedback

def normalise_scores(scores):

	"""
	Divides feature counts by 100 words/tokens
	"""

	token_count = list(scores['Counts'][scores['Features'] == 'Token_count'])[0]
	scores['Counts_norm'] = scores['Counts'] / token_count * 100

	return scores


def extract_features(text):

	start_time = time.process_time()

	scores = fe.feat_counts(text, kw)
	scores = normalise_scores(scores)

	
	# imp_feats, recog_feats = top_bottom_feats(scores)
	scores = top_bottom_feats(scores)


	# improvement = get_main_response(imp_feats)
	# recognition = get_recognition(recog_feats)
	feedback = get_feedback(scores)


	jsondata = json.dumps(
		{
		"Acknowledgement": feedback[0],
		"Agreement": feedback[1],
		"Hedges": feedback[2],
		"Negation": feedback[3],
		"Positive_Emotion": feedback[4],
		"Reasoning": feedback[5],
		"Subjectivity": feedback[6],
		"Adverb_Limiter": feedback[7],
		"Second_Person": feedback[8],
		})
	delta = round(time.process_time() - start_time, 3)
	print('Runtime: ', delta)

	return jsondata


if __name__ == "__main__":

	text = 'I feel like there should be more regulations with guns. I feel that cops shouldnt be allowed to kill. Why cant they just injure the individual?'
	feedback = extract_features(text)
	print(feedback)








