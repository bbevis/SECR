
import regex
import re

import nltk
from nltk.corpus import stopwords
from nltk import tokenize

import pandas as pd
import numpy as np

from category_counts import politeness
import prep

test_data = {
			'Branding': 
				{'Kate': 
					{'Headlines': 'Kate and Wills Inc: Duke and Duchess secretly set up companies to protect their brand - just like the Beckhams',
					'Date': '2014-01-17',
					'Publisher': 'Daily Mail'},
				'Meghan': 
					{'Headlines': 'A right royal cash in! How Prince Harry and Meghan Markle trademarked over 100 items from hoodies to socks \
					SIX MONTHS before split with monarchy - with new empire worth up to £400m',
					'Date': '2020-01-09',
					'Publisher': 'Daily Mail'}},
			'Bump': 
				{'Kate': 
					{'Headlines': 'Not long to go! Pregnant Kate tenderly cradles her baby bump while wrapping up her \
					royal duties ahead of maternity leave - and William confirms she\'s due \'any minute now\'',
					'Date': '2018-03-22',
					'Publisher': 'Daily Mail'},
				'Meghan': 
					{'Headlines': 'Why can\'t Meghan Markle keep her hands off her bump? Experts tackle the question \
					that has got the nation talking: Is it pride, vanity, acting - or a new age bonding technique?',
					'Date': '2019-01-26',
					'Publisher': 'Daily Mail'}},
			'Avocado': 
				{'Kate': 
					{'Headlines': 'Kate’s morning sickness cure? Prince William gifted with an avocado for pregnant Duchess',
					'Date': '2017-07-14',
					'Publisher': 'The Express'},
				'Meghan': 
					{'Headlines': 'Meghan Markle’s beloved avocado linked to human rights abuse and drought, millennial shame',
					'Date': '2019-01-23',
					'Publisher': 'The Express'}},
			'Stiff': 
				{'Kate': 
					{'Headlines': 'STIFF UPPER FLIP Prince William blasts monarchy’s ‘stiff upper lip’ tradition and \
					backs Harry’s admission of his mental anguish after death of mother Diana',
					'Date': '2017-04-18',
					'Publisher': 'The Sun'},
				'Meghan': 
					{'Headlines': 'ROYAL RIFTS Prince Harry and Meghan ditched British stiff upper lip – is this a good thing? Sun parents and kids are torn',
					'Date': '2019-10-23',
					'Publisher': 'The Sun'}},
			'Christmas': 
				{'Kate': 
					{'Headlines': 'Carole wins granny war! Duke and Duchess of Cambridge will spend second \'private\' \
					Christmas with the Middleton family rather than joining the Queen at Sandringham',
					'Date': '2016-12-16',
					'Publisher': 'Daily Mail'},
				'Meghan': 
					{'Headlines': 'Doesn\'t the Queen deserve better than this baffling festive absence? RICHARD KAY examines the impact of \
					Prince Harry and Meghan Markle\'s decision not to spend Christmas with the royal family',
					'Date': '2019-11-13',
					'Publisher': 'Daily Mail'}},
			'Candles': 
				{'Kate': 
					{'Headlines': 'Ladies in waiting! Kate\'s £70 wedding day fragrance sells out as fans worldwide snap up last bottles',
					'Date': '2011-05-05',
					'Publisher': 'Daily Mail'},
				'Meghan': 
					{'Headlines': 'Kicking up a stink: \'Dictatorial\' bride Meghan wanted air fresheners for \'musty\' 15th-century St George\'s Chapel... but the Palace said no',
					'Date': '2018-11-30',
					'Publisher': 'Daily Mail'}},
			'Flowers': 
				{'Kate': 
					{'Headlines': 'Why you can always say it with flowers',
					'Date': '2011-09-29',
					'Publisher': 'The Express'},
				'Meghan': 
					{'Headlines': 'Royal wedding: How Meghan Markle’s flowers may have put Princess Charlotte’s life at risk',
					'Date': '2019-10-13',
					'Publisher': 'The Express'}},
			'Christening': 
				{'Kate': 
					{'Headlines': 'Beaming Kate gazes lovingly at sleeping Prince Louis as she and William attend his christening \
					in their first appearance as a family of five (but the Queen misses big day)',
					'Date': '2018-07-09',
					'Publisher': 'Daily Mail'},
				'Meghan': 
					{'Headlines': 'Revealed: The Queen won\'t be at Archie\'s christening because Meghan, \
					Harry and the mystery godparents planned to baptize him TODAY but had to rearrange when they realised Her Majesty and Prince Charles were already busy',
					'Date': '2019-07-05',
					'Publisher': 'Daily Mail'}},
			'Fashion Queen': 
				{'Kate': 
					{'Headlines': 'Kate\'s stylish coat co-ordinated perfectly with the Queen',
					'Date': '2013-02-14',
					'Publisher': 'The Mirror'},
				'Meghan': 
					{'Headlines': 'How Meghan Markle\'s confusion over a hat nearly got her into big trouble with the Queen',
					'Date': '2018-10-29',
					'Publisher': 'The Mirror'}},
			'Style': 
				{'Kate': 
					{'Headlines': 'SARAH VINE: How Kate went from drab to fab! From eyebrows and pilates to a new style guru, \
					our experts reveal the Duchess of Cambridge\'s secrets to looking sizzling',
					'Date': '2019-06-16',
					'Publisher': 'Daily Mail'},
				'Meghan': 
					{'Headlines': 'SARAH VINE: My memo to Meghan Markle following her Vogue editorial - we Brits prefer true royalty to fashion royalty',
					'Date': '2019-17-29',
					'Publisher': 'Daily Mail'}}

			}




categories = list(test_data.keys())

def politenes_scores(name):

	for c in range(len(categories)):

		text = test_data[categories[c]][name]['Headlines']
		prep.prep_whole(text)
		#print(text)
		pol = politeness(text, level = 'Phrase')
		score = pol.main()
		if c == 0:
			scores = score
		else:
			scores = pd.concat([scores, score], axis = 1)

	scores.columns = categories
	scores = scores.fillna(0)
	return scores


Kate_res = politenes_scores('Kate')
Meg_res = politenes_scores('Meghan')

Kate_res.to_csv('Kate test.csv')
Meg_res.to_csv('Meg test.csv')
#print(Kate_res)
