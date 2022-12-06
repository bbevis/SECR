import os
import time


#--- VARS ---#
PATH = '../Data/'
UPLOAD_FOLDER = '../Data/In/'
DOWNLOAD_FOLDER = '../data/Out/'
ALLOWED_EXTENSIONS = set(['.txt'])

FOLDERS_IN = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']
READ_TYPE = ['single', 'multiple', 'multiple', 'single', 'single', 'single']


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
