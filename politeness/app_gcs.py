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
#from negspacy.negation import Negex


#--- VARS ---#
PATH = '../Data/'
UPLOAD_FOLDER	 = '../Data/In/'
DOWNLOAD_FOLDER	 = '../data/Out/'
ALLOWED_EXTENSIONS = set(['.txt'])

FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']
READ_TYPE  = ['single', 'multiple', 'multiple', 'single', 'single', 'single']

main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity', 'First_Person_Single', 'Second_Person']
thresholds = [0, 1, 2, 2, 3, 0, 1, 2, 1]

cgitb.enable()
form = cgi.FieldStorage()
#text = form['text'].value 

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
	

	scores['diff'] = scores['Counts'] - scores['thresholds']
	scores = scores.sort_values('diff')

	imp_feats = list(scores['Features'][:3])
	#bottom3 = list(scores['Features'][-3:])

	recog_feats = scores['Features'][scores['Counts'] > 0]

	return imp_feats, recog_feats

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


def extract_features(text):

	start_time = time.process_time()

	scores = fe.feat_counts(text, kw)

	imp_feats, recog_feats = top_bottom_feats(scores)
	improvement = get_main_response(imp_feats)
	recognition = get_recognition(recog_feats)


	# jsondata = json.dumps(
	# 	{
	# 	"r1": recognition[0],
	# 	"r2": recognition[1],
	# 	"r3": recognition[2],
	# 	"r4": recognition[3],
	# 	"r5": recognition[4],
	# 	"r6": recognition[5],
	# 	"r7": recognition[6],
	# 	"r8": recognition[7],
	# 	"r9": recognition[8],
	# 	"imp1": improvement[0],
	# 	"imp2": improvement[1],
	# 	"imp3": improvement[2]
	# 	})
	# delta = round(time.process_time() - start_time, 3)
	# print('Runtime: ', delta)

	# return jsondata


if __name__ == "__main__":

	text = 'I\'m not quite sure I really understand sorry, but for me please could you let me know how you came to this way of thinking? Would you mind?'
	# feedback = extract_features(text)
	extract_features(text)
	# print(feedback)








