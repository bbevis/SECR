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
#from negspacy.negation import Negex

app = Flask(__name__)

#--- VARS ---#
PATH = '../Data/'
UPLOAD_FOLDER	 = '../Data/In/'
DOWNLOAD_FOLDER	 = '../data/Out/'
ALLOWED_EXTENSIONS = set(['.txt'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limit files sizes to 16 MBs. Flask will raise a RequestEntityTooLarge exception.
app.secret_key = '514609ea9026b3956660d714'

FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_neg', 'word_start']
READ_TYPE  = ['single', 'multiple', 'multiple', 'single']

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

#--- ROUTES ---#

@app.route('/')
def home():
	return ""

@app.route('/commit', methods=['POST'])
def commit_new_data():

	start_time = time.process_time()

	
	create_in()
	prep.commit_data(PATH, UPLOAD_FOLDER, FOLDERS_IN, READ_TYPE)
	delta = round(time.process_time() - start_time, 3)

	#print('Data uploaded in %.3f seconds' % delta)

	#flash('Data uploaded in %.3f seconds' % delta, 'category1')


@app.route('/extract_features', methods=['POST'])
def extract_features():

	start_time = time.process_time()

	text = request.form['text']
	#text = 'I\'m not quite sure I really understand sorry, but for me please could you let me know how you came to this way of thinking? Would you mind?'

	scores = fe.feat_counts(text, kw)

	top3 = list(scores['Features'][:3])

	#bottom3 = list(scores['Features'][-3:])

	f1 = 'To avoid spiraling conflict, use more '
	f2 = ', '.join(top3)
	f3 = ' words'
	feedback = f1 + f2 + f3


	delta = round(time.process_time() - start_time, 3)

	# flash('Features extracted in %.3f seconds' % delta, 'category1')

	# flash(feedback, 'category1')

	jsondata = '{"message": "' + feedback + '"}'

	return jsonify(jsondata)


if __name__ == "__main__":
	app.run(debug=True)
	#commit_new_data()
	#extract_features()








