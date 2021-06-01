import os
import time
import pandas as pd
import prep
#from sentiment import Sentiment
import feature_extraction as fe
import spacy
import en_core_web_sm
from flask import Flask, request, jsonify, render_template, flash
from flask import redirect, url_for, send_from_directory, send_file, Response
import urllib.request
import json
import responses
import re
#from negspacy.negation import Negex

app = Flask(__name__)

#--- VARS ---#
PATH = '../Data/'
UPLOAD_FOLDER	 = '../Data/In/'
DOWNLOAD_FOLDER	 = '../data/Out/'
ALLOWED_EXTENSIONS = set(['.txt'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limit files sizes to 16 MBs. Flask will raise a RequestEntityTooLarge exception.
app.secret_key = '514609ea9026b3956660d714'

FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']
READ_TYPE  = ['single', 'multiple', 'multiple', 'single', 'single', 'single']

main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity']
thresholds = [0, 1, 2, 2, 3, 0, 1]

nlp = en_core_web_sm.load()

# kw is a dictionary of all key words, dependency pairs and negation words
kw = prep.load_saved_data(UPLOAD_FOLDER, FOLDERS_IN)

#--- FUNCTIONS ---#

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_in():
	if not os.path.exists(UPLOAD_FOLDER):
		os.makedirs(UPLOAD_FOLDER)

def create_out():
	if not os.path.exists(DOWNLOAD_FOLDER):
		os.makedirs(DOWNLOAD_FOLDER)

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
	mid_term1 = ' in your response helps the other person in a debate to be more open and receptive to you. \n' 
	mid_term2 = ' To increase receptiveness further, try adding more '
	end = '.This will help you maintain your relationships when dealing with difficult subjects.'
	feedback = intro + recognition + mid_term1 + mid_term2 + main_response + end

	return feedback

#--- ROUTES ---#

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/commit', methods=['POST'])
def commit_new_data():

	start_time = time.process_time()

	
	create_in()
	prep.commit_data(PATH, UPLOAD_FOLDER, FOLDERS_IN, READ_TYPE)
	delta = round(time.process_time() - start_time, 3)

	#print('Data uploaded in %.3f seconds' % delta)

	flash('Data uploaded in %.3f seconds' % delta, 'category1')


@app.route('/extract_features', methods=['POST'])
def extract_features():

	start_time = time.process_time()

	text = request.form['text']

	scores = fe.feat_counts(text, kw)

	top3, bottom3 = top_bottom3(scores)
	main_response = get_main_response(top3)
	recognition = get_recognition(bottom3)
	feedback = feedback_text(main_response, recognition)

	jsondata = json.dumps({"message": feedback})
	delta = round(time.process_time() - start_time, 3)

	flash('Features extracted in %.3f seconds' % delta, 'category1')

	flash(feedback, 'category1')

	return redirect('/')


if __name__ == "__main__":
	app.run(debug=True)
	#commit_new_data()
	#extract_features()








