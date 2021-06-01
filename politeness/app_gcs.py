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
import requests
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

main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity']
thresholds = [0, 1, 2, 2, 3, 0, 1]

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


def top_bottom3(scores):

	scores = scores[scores['Features'].isin(main_features)]
	cutoffs = pd.DataFrame({
		'main_features': main_features,
		'thresholds': thresholds
		})
	scores = pd.merge(scores, cutoffs, left_on = 'Features', right_on='main_features', how = 'left')
	

	scores['diff'] = scores['Counts'] - scores['thresholds']
	scores = scores.sort_values('diff')

	top3 = list(scores['Features'][:3])
	bottom3 = list(scores['Features'][-3:])

	return top3, bottom3

def get_main_response(top3):

	top3_feats = [responses.fancy_responses[top3[i]]['fancy_name'] for i in range(len(top3))]
	top3_examples = [responses.fancy_responses[top3[i]]['examples'] for i in range(len(top3))]
	main_response = [a + ' ' + b for a, b in zip(top3_feats, top3_examples)]
	main_response = ', '.join(main_response)
	main_response = re.sub(r',', 'dna ', main_response[::-1], 1)[::-1]

	return main_response

def get_recognition(bottom3):

	bottom3_feats = [responses.fancy_responses[bottom3[i]]['fancy_name'] for i in range(len(bottom3))]
	recognition = ', '.join(bottom3_feats)
	recognition = re.sub(r',', 'dna ', recognition[::-1], 1)[::-1]

	return recognition

def feedback_text(main_response, recognition):

	intro = 'Well done! Using '
	mid_term = ' in your response helps the other person in a debate to be more open and receptive to you. To increase receptiveness further, try adding more ' 
	end = '. This will help you maintain your relationships when dealing with difficult subjects.'
	feedback = intro + recognition + mid_term + main_response + end

	return feedback

def extract_features(text):

	start_time = time.process_time()

	scores = fe.feat_counts(text, kw)

	top3, bottom3 = top_bottom3(scores)
	main_response = get_main_response(top3)
	recognition = get_recognition(bottom3)
	feedback = feedback_text(main_response, recognition)

	jsondata = json.dumps({"message": feedback})
	delta = round(time.process_time() - start_time, 3)
	print('Runtime: ', delta)

	return jsondata


if __name__ == "__main__":

	text = 'I\'m not quite sure I really understand sorry, but for me please could you let me know how you came to this way of thinking? Would you mind?'
	feedback = extract_features(text)
	print(feedback)








