import time
import prep
import pandas as pd
#from sentiment import Sentiment
import feature_extraction as fe
import spacy
import en_core_web_sm
#from negspacy.negation import Negex

nlp = en_core_web_sm.load()

start_time = time.clock()

text = 'I don\'t understand what you mean, but for me please could you let me know how you came to this way of thinking? Would you mind?'
clean_text = prep.prep_simple(text)
doc = nlp(clean_text)

PATH = '../Data/'
UPLOAD_FOLDER	 = '../Data/In/'
DOWNLOAD_FOLDER	 = '../data/Out/'
FOLDERS_IN 	 = ['word_matches', 'spacy_pos', 'spacy_neg', 'word_start']
READ_TYPE  = ['single', 'multiple', 'multiple', 'single']


#prep.commit_data(path, folders, words_in_line)
kw = prep.load_saved_data(UPLOAD_FOLDER, FOLDERS_IN)

#print(kw['word_matches'])
sc1 = fe.count_matches(kw['word_matches'], text)
#print(count_matches)

# Includes negation handling
dep_pairs = fe.get_dep_pairs(doc)
print(dep_pairs)

#print(dep_pairs)
sc2 = fe.count_spacy_matches(kw['spacy_pos'], dep_pairs)

scores = pd.concat([sc1,sc2])
#print(scores)

scores = scores.groupby('Features').sum().sort_values(by = 'Counts', ascending = False)
scores = scores.reset_index()
#print(scores)

top3 = list(scores['Features'][:3])
#print(top3)

bottom3 = list(scores['Features'][-3:])
#print(bottom3)

f1 = 'You scored well on receptiveness through the use of '
f2 = ', '.join(top3)
f3 = '. However, consider using more '
f4 = ', '.join(bottom3)
f5 = ' to increase openess and receptiveness'
feedback = f1 + f2 + f3 + f4 + f5

#print(feedback)

#print(sc1)
#print(sc2)
print(round(time.clock() - start_time, 3), "seconds")










