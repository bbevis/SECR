
import os
import pandas as pd
import prep
import spacy
import en_core_web_sm
import re

nlp = en_core_web_sm.load()


def count_matches(keywords, text):

	"""
	For a given piece of text, search for the number if keywords from a prespecified list

	Inputs:
		Prespecified list (keywords)
		text

	Outputs:
		Counts of keyword matches
	"""

	key_res = []
	phrase2_count = []

	for key in keywords:
		
		key_res.append(key)
		counter = 0

		check = any(item in text for item in keywords[key])

		if check == True:

			for phrase in keywords[key]:

				phrase_count = text.count(phrase)

				if phrase_count > 0:

					counter = counter + phrase_count

		phrase2_count.append(counter)

	res = pd.DataFrame([key_res, phrase2_count], index = ['Features', 'Counts']).T

	return res

def get_dep_pairs(doc):

	"""
	Uses spaCy to find list of dependency pairs from text

	Input:
		Text

	Outputs:
		Dependency pairs from next that do not have ROOT as the head token or is a negated term
	"""

	dep_pairs = [[token.dep_, token.head.text, token.head.i, token.text, token.i] for token in doc]
	negations = [dep_pairs[i] for i in range(len(dep_pairs)) if dep_pairs[i][0] == 'neg']

	dep_pairs2 = []

	if len(negations) > 0:
		for i in range(len(negations)):
			for j in range(len(dep_pairs)):

				if negations[i][1] != dep_pairs[j][1] and negations[i][2] != dep_pairs[j][2] and dep_pairs[j][0] not in ['ROOT','neg']:
					dep_pairs2.append([dep_pairs[j][0], dep_pairs[j][1], dep_pairs[j][3]])
	else:
		for j in range(len(dep_pairs)):

			# When there are no negations, just remove all root
			if dep_pairs[j][0] != 'ROOT':
				dep_pairs2.append([dep_pairs[j][0], dep_pairs[j][1], dep_pairs[j][3]])

	return dep_pairs2

def get_dep_pairs_noneg(doc):

	dep_pairs = [[token.dep_, token.head.text, token.head.i, token.text, token.i] for token in doc]

	dep_pairs2 = []
	for j in range(len(dep_pairs)):

		if dep_pairs[j][0] != 'ROOT':
			dep_pairs2.append([dep_pairs[j][0], dep_pairs[j][1], dep_pairs[j][3]])

	return dep_pairs2

def count_spacy_matches(keywords, dep_pairs, dep_pairs_noneg):

	"""
	When searching for key words are not sufficient, we may search for dependency pairs.
	Finds any-prespecified dependency pairs from text string and outputs the counts

	Inputs:
		Dependency pairs from text
		Predefined tokens for search in dependency heads

	Output:
		Count of dependency pair matches
	"""

	key_res = []
	phrase2_count = []

	for key in keywords:

		if key == 'Disagreement':

			dep_pairs_final = dep_pairs_noneg.copy()
		else:
			dep_pairs_final = dep_pairs.copy()


		key_res.append(key)
		counter = 0

		check = any(item in dep_pairs_final for item in keywords[key])
		if check == True:

			for phrase in keywords[key]:

				if phrase in dep_pairs_final:
					
					for dep in dep_pairs_final:

						if phrase == dep:

							counter = counter + 1

		phrase2_count.append(counter)

	res = pd.DataFrame([key_res, phrase2_count], index = ['Features', 'Counts']).T

	return res

def token_count(doc):

	# Counts number of words in a text string
	return len([token for token in doc])

def bare_command(text):

	"""
	Check the first word of each sentence is a verb AND is contained in list of key words

	Output: Count of matches
	"""

	keywords = set(['be', 'do', 'please', 'have', 'thank', 'hang', 'let'])

	nlp.enable_pipe("senter")
	doc = nlp(text)

	# Returns first word of every sentence along with the corresponding POS
	first_words = [str(sent[0]) for sent in doc.sents]
	POS_fw = [sent[0].pos_ for sent in doc.sents]

	# clean text
	first_words = [prep.prep_simple(str(fw)) for fw in first_words]

	# returns word if word is a verb and in list of keywords
	first_words = [b for a, b in zip(POS_fw, first_words) if a == 'VERB' and b not in keywords]

	return len(first_words)


def WHQuestion(doc):

	"""
	Counts number of prespecified question words
	"""

	keywords = set(["who","what","where","when","why","how","which"])

	words = [str(token) for token in doc]
	words = [i for i in words if i in keywords]

	return len(words)

def YesNoQuestions(text, whq):

	"""
	Counts number of question marks and subtracts number of key question words
	"""
	return text.count("?") - whq

def word_start(keywords, doc):

	"""
	Find first words in text such as conjunctions and affirmations
	"""

	key_res = []
	phrase2_count = []

	for key in keywords:

		first_words = [str(sent[0]) for sent in doc.sents]
		first_words = [prep.prep_simple(str(fw)) for fw in first_words]

		cs = [w for w in first_words if w in keywords[key]]
		phrase2_count.append(len(cs))
		key_res.append(key)

	
	res = pd.DataFrame([key_res, phrase2_count], index = ['Features', 'Counts']).T

	return res


def feat_counts(text, kw):

	"""
	Main function for getting the features from text input.
	Calls other functions to load dataset, clean text, counts features,
	removes negation phrases.

	Input:
		Text string
		Saved data of keywords and dependency pairs from pickle files

	Output:
		Feature counts
	"""

	clean_text = prep.prep_simple(text)

	doc = nlp(clean_text)
	
	# Count key words and dependency pairs with negation
	kw_matches = count_matches(kw['word_matches'], clean_text)

	dep_pairs = get_dep_pairs(doc)
	dep_pairs_noneg = get_dep_pairs_noneg(doc)
	dep_pairs = count_spacy_matches(kw['spacy_pos'], dep_pairs, dep_pairs_noneg)

	# count start word matches like conjunctions and affirmations
	start_matches = word_start(kw['word_start'], doc)

	scores = pd.concat([kw_matches, dep_pairs, start_matches])
	scores = scores.groupby('Features').sum().sort_values(by = 'Counts', ascending = False)
	scores = scores.reset_index()

	# add remaining features
	bc = bare_command(text)
	scores.loc[len(scores)] = ['Bare_Command', bc]

	# whq = WHQuestion(doc)
	# scores.loc[len(scores)] = ['WH_Questions', whq]

	ynq = len(scores['Counts'][scores['Features'] == 'WH_Questions'])
	scores.loc[len(scores)] = ['YesNo_Questions', ynq]

	scores = scores.sort_values(by = 'Counts', ascending = False)

	tokens = token_count(doc)
	scores.loc[len(scores)] = ['Token_count', tokens]

	return scores



if __name__ == '__main__':

	UPLOAD_FOLDER	 = '../Data/In/'
	FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_neg', 'word_start']

	text = 'yes I agree, it is letting a woman decide for herself what is best for her.  If she wants to be a stay at home mom, at least she made the choice for herself.  And while I agree that in a perfect world, women and men would have equal footing being hired, that is never the case.  Women are taught to be submissive, to be accepting of all outcomes, to not be advocates for themselves, especially in the workforce.  Women need the extra boost to be hired in STEM fields so children can see that they really can do and be anything they want.'
	# kw is a dictionary of all key words, dependency pairs and negation words
	kw = prep.load_saved_data(UPLOAD_FOLDER, FOLDERS_IN)
	scores = feat_counts(text, kw)
	print(scores)





