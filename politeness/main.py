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
import random

from flask import Flask, request


app = Flask(__name__)

#--- VARS ---#
# PATH = '../Data/'
# UPLOAD_FOLDER = '../Data/In/'
# DOWNLOAD_FOLDER = '../data/Out/'
# ALLOWED_EXTENSIONS = set(['.txt'])

# FOLDERS_IN = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']
# READ_TYPE = ['single', 'multiple', 'multiple', 'single', 'single', 'single']

main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity', 'Adverb_Limiter', 'Disagreement']
main_features_pos = ['Acknowledgement', 'Agreement', 'Hedges', 'Positive_Emotion', 'Subjectivity']
main_features_neg = ['Negation', 'Reasoning', 'Adverb_Limiter', 'Disagreement']

thresholds = [0.0, 1.1, 1.4, 1.4, 2.9, 0.0, 0.0, 0.0, 0.0]


# nlp = en_core_web_sm.load()

# kw is a dictionary of all key words, dependency pairs and negation words
#kw = prep.load_saved_data(UPLOAD_FOLDER, FOLDERS_IN)
#print(json.dumps(kw,sort_keys=True, indent=4))

kw = keywords.kw
# print(kw)

#--- HELPER FUNCTIONS ---#


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def create_in():
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)


# def create_out():
#     if not os.path.exists(DOWNLOAD_FOLDER):
#         os.makedirs(DOWNLOAD_FOLDER)

#--- MAIN FUNCTIONS ---#

#
# def commit_new_data():

#     prep.commit_data(PATH, UPLOAD_FOLDER, FOLDERS_IN, READ_TYPE)


def get_scores(scores, ordered=None):
    """
    Returns dataframe of Features along with their scores
    """

    scores = scores[scores['Features'].isin(main_features)]
    cutoffs = pd.DataFrame({
        'main_features': main_features,
        'thresholds': thresholds
    })
    scores = pd.merge(scores, cutoffs, left_on='Features', right_on='main_features', how='left')

    scores['diff'] = scores['Counts_norm'] - scores['thresholds']

    if ordered == 'ranked':
        scores['abs_diff'] = abs(scores['diff'])
        scores['ranked_diff'] = [scores['diff'][x] * -1
                                 if scores['Features'][x] in main_features_pos and scores['diff'][x] != 0
                                 else scores['diff'][x] * -1 + 0.001  # this is the tie breaker
                                 if scores['Features'][x] in main_features_pos and scores['diff'][x] == 0
                                 else scores['diff'][x]
                                 for x in range(scores['Features'].shape[0])]

        scores = scores.sort_values('ranked_diff', ascending=False)

    if ordered == 'random':
        scores = scores.sample(frac=1).reset_index(drop=True)

    return scores


def get_feedback(scores):
    """
    Returns a list of responses for the recognition features if in recog_feats list
    otherwise returns a response from the improvment list
    """

    feedback = []

    ordered_features = scores['Features'].tolist()

    for i in ordered_features:
        diff = scores['diff'].loc[scores['Features'] == i].to_list()[0]
        if i in main_features_pos and diff <= 0:
            feedback.append(responses.fancy_responses[i]['imp'])
        elif i in main_features_pos and diff > 0:
            feedback.append(responses.fancy_responses[i]['recog'])
        elif i in main_features_neg and diff > 0:
            feedback.append(responses.fancy_responses[i]['imp'])
        elif i in main_features_neg and diff <= 0:
            feedback.append(responses.fancy_responses[i]['recog'])

    return feedback


def normalise_scores(scores):
    """
    Divides feature counts by 100 words/tokens
    """

    token_count = list(scores['Counts'][scores['Features'] == 'Token_count'])[0]
    scores['Counts_norm'] = scores['Counts'] / token_count * 100

    return scores


@app.route("/", methods=['GET', 'POST'])
def extract_features():

    start_time = time.process_time()

    text = request.args.get('text', None)
    ordered = request.args.get('ordered', None)

    scores = fe.feat_counts(text, kw)
    scores = normalise_scores(scores)

    if ordered is None:
        scores = get_scores(scores)
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
                "Disagreement": feedback[8],
            })

    if ordered == 'ranked':

        scores = get_scores(scores, ordered='ranked')

        feedback = get_feedback(scores)

        ranked_features = scores['Features'].tolist()

        jsondata = json.dumps(
            {
                "message_1": feedback[0],
                "message_2": feedback[1],
                "message_3": feedback[2],
                "message_4": feedback[3],
                "message_5": feedback[4],
                "message_6": feedback[5],
                "message_7": feedback[6],
                "message_8": feedback[7],
                "message_9": feedback[8],
                "feature_name_1": ranked_features[0],
                "feature_name_2": ranked_features[1],
                "feature_name_3": ranked_features[2],
                "feature_name_4": ranked_features[3],
                "feature_name_5": ranked_features[4],
                "feature_name_6": ranked_features[5],
                "feature_name_7": ranked_features[6],
                "feature_name_8": ranked_features[7],
                "feature_name_9": ranked_features[8],
            })

    if ordered == 'random':

        scores = get_scores(scores, 'random')

        feedback = get_feedback(scores)

        ranked_features = scores['Features'].tolist()

        jsondata = json.dumps(
            {
                "message_1": feedback[0],
                "message_2": feedback[1],
                "message_3": feedback[2],
                "message_4": feedback[3],
                "message_5": feedback[4],
                "message_6": feedback[5],
                "message_7": feedback[6],
                "message_8": feedback[7],
                "message_9": feedback[8],
                "feature_name_1": ranked_features[0],
                "feature_name_2": ranked_features[1],
                "feature_name_3": ranked_features[2],
                "feature_name_4": ranked_features[3],
                "feature_name_5": ranked_features[4],
                "feature_name_6": ranked_features[5],
                "feature_name_7": ranked_features[6],
                "feature_name_8": ranked_features[7],
                "feature_name_9": ranked_features[8],
            })

    print(scores)
    print(scores['thresholds'])
    delta = round(time.process_time() - start_time, 3)
    print('Runtime: ', delta)

    return jsondata


if __name__ == "__main__":

    app.run(debug=True)

    # text = 'I agree that social media has done nothing to improve the dialogue between all involved parties, and may have contributed to a greater divide between the two factions. However, I think that social media can help to spread awareness of these incidents. The more publicity the confrontation of police and minority crime suspects get, the more likely there will be consequences (e.g. if the police officers used unnecessary force). I hope in the long-term, this might have a positive impact on our police policies.'
    # feedback = extract_features(text, ordered='ranked')
    # print(feedback)
