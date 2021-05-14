

import nltk
from nltk.corpus import stopwords
from nltk import tokenize
import regex
import re
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

import numpy as np
import pandas as pd
import os

import prep
import nltkmodules



class Sentiment():
	"""docstring for ClassName"""

	def __init__(self, text):

		self.text = text

		self.high_polarity = 0.1
		self.low_polarity = -0.1
		self.high_subjectivity = 0.6
		self.low_subjectivity = 0.4
	
	def polarity(self, phrases):

		# get list of words that are positive, negative and neutral
		# return counts for each of the three categories

		pos_pol_list = []
		neg_pol_list = []

		pos_pol_score = []
		neg_pol_score = []

		for phrase in phrases:
			blob = TextBlob(phrase)
			# print(blob.tags)
			if blob.sentiment.polarity >= self.high_polarity:
				pos_pol_list.append(phrase)
				pos_pol_score.append(blob.sentiment.polarity)

			elif blob.sentiment.polarity <= self.low_polarity:
				neg_pol_list.append(phrase)
				neg_pol_score.append(blob.sentiment.polarity)

		#print(pol_phrases)

		scores = [round(np.mean(pos_pol_score), 2), round(np.mean(neg_pol_score), 2)]
		counts = [len(pos_pol_score), len(neg_pol_score)]

		return scores, counts

	def subjectivity(self, phrases):

		pos_sub_list = []
		neg_sub_list = []

		pos_sub_score = []
		neg_sub_score = []

		for phrase in phrases:
			blob = TextBlob(phrase)

			if blob.sentiment.subjectivity >= self.high_subjectivity:
				pos_sub_list.append(phrase)
				pos_sub_score.append(blob.sentiment.subjectivity)

			elif blob.sentiment.subjectivity <= self.low_subjectivity:
				neg_sub_list.append(phrase)
				neg_sub_score.append(blob.sentiment.subjectivity)

		scores = [round(np.mean(pos_sub_score), 2), round(np.mean(neg_sub_score), 2)]
		counts = [len(pos_sub_score), len(neg_sub_score)]

		return scores, counts

	def scores(self):

		#text = prep.phrase_split(self.text) # Change to sentence split from SpaCy

		pol_scores, pol_counts = self.polarity(self.text)
		sub_scores, sub_counts = self.subjectivity(self.text)

		
		key_res = ['highPolarity_score', 'lowPolarity_score', 'highPolarity_count','lowPolarity_count',
		'highSubjectivity_score', 'lowSubjectivity_score', 'highSubjectivity_count', 'lowSubjectivity_count']

		sentiment_res = [pol_scores[0], pol_scores[1], pol_counts[0], pol_counts[1],
		sub_scores[0],sub_scores[1], sub_counts[0], sub_counts[1]]

		res = pd.DataFrame(sentiment_res, index = key_res)

		return res


if __name__ == '__main__':

	text = 'I\'m not quite sure I understand for me, please could you let me know how you came to this way of thinking? Would you mind?'
	
	clean_text = prep.sentenciser(text)
	#clean_text = prep.phrase_split(text)
	clean_text = [prep.prep_simple(t) for t in clean_text]

	se = Sentiment(clean_text)
	sent = se.sentiment()

	
	#df = pd.concat(sent, axis = 0)
	print(sent)


