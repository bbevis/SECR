
import os
import pandas as pd
import prep
import spacy
import en_core_web_sm
import re
import numpy as np
import keywords

nlp = en_core_web_sm.load()
nlp.enable_pipe("senter")


def sentence_split(doc):

    # doc = nlp(text)
    sentences = [str(sent) for sent in doc.sents]
    sentences = [' ' + prep.prep_simple(str(s)) + ' ' for s in sentences]

    return sentences


def sentence_pad(doc):

    sentences = sentence_split(doc)

    return ''.join(sentences)


def count_matches(keywords, doc):
    """
    For a given piece of text, search for the number if keywords from a prespecified list

    Inputs:
            Prespecified list (keywords)
            text

    Outputs:
            Counts of keyword matches
    """

    text = sentence_pad(doc)

    # print(text)

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

    res = pd.DataFrame([key_res, phrase2_count], index=['Features', 'Counts']).T

    return res


def get_dep_pairs(doc):
    """
    Uses spaCy to find list of dependency pairs from text.
    Performs negation handling where by any dependency pairs related to a negated term is removed

    Input:
            Text

    Outputs:
            Dependency pairs from text that do not have ROOT as the head token or is a negated term
    """

    dep_pairs = [[token.dep_, token.head.text, token.head.i, token.text, token.i] for token in doc]

    # print(dep_pairs)

    negations = [dep_pairs[i] for i in range(len(dep_pairs)) if dep_pairs[i][0] == 'neg']
    token_place = [dep_pairs[i][2] for i in range(len(dep_pairs)) if dep_pairs[i][0] == 'neg']

    dep_pairs2 = []

    # if len(negations) > 0:
    # 	for i in range(len(negations)):
    # 		for j in range(len(dep_pairs)):

    # 			if negations[i][2] != dep_pairs[j][2] and dep_pairs[j] not in dep_pairs2:
    # 				dep_pairs2.append(dep_pairs[j])

    if len(negations) > 0:

        for j in range(len(dep_pairs)):

            if dep_pairs[j][2] not in token_place and dep_pairs[j] not in dep_pairs2:
                dep_pairs2.append(dep_pairs[j])

    else:
        dep_pairs2 = dep_pairs.copy()

    dep_pairs2 = [[dep_pairs2[i][0], dep_pairs2[i][1], dep_pairs2[i][3]] for i in range(len(dep_pairs2))]

    return dep_pairs2, negations


def get_dep_pairs_noneg(doc):
    """
    No negation is done as we are only searching 'hits'
    """
    return [[token.dep_, token.head.text, token.text] for token in doc]


def count_spacy_matches(keywords, dep_pairs):
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
        # print(key)

        key_res.append(key)
        counter = 0

        check = any(item in dep_pairs for item in keywords[key])

        if check == True:

            for phrase in keywords[key]:

                if phrase in dep_pairs:

                    for dep in dep_pairs:

                        if phrase == dep:

                            counter = counter + 1

        phrase2_count.append(counter)

    res = pd.DataFrame([key_res, phrase2_count], index=['Features', 'Counts']).T

    return res


def token_count(doc):

    # Counts number of words in a text string
    return len([token for token in doc])


def bare_command(doc):
    """
    Check the first word of each sentence is a verb AND is contained in list of key words

    Output: Count of matches
    """

    keywords = set([' be ', ' do ', ' please ', ' have ', ' thank ', ' hang ', ' let '])

    # nlp.enable_pipe("senter")
    #doc = nlp(text)

    # Returns first word of every sentence along with the corresponding POS
    first_words = [' ' + prep.prep_simple(str(sent[0])) + ' ' for sent in doc.sents]

    POS_fw = [sent[0].tag_ for sent in doc.sents]

    # returns word if word is a verb and in list of keywords
    bc = [b for a, b in zip(POS_fw, first_words) if a == 'VB' and b not in keywords]

    return len(bc)


def Question(doc):
    """
    Counts number of prespecified question words
    """

    keywords = set([' who ', ' what ', ' where ', ' when ', ' why ', ' how ', ' which '])
    tags = set(['WRB', 'WP', 'WDT'])

    # doc = nlp(text)
    sentences = [str(sent) for sent in doc.sents if '?' in str(sent)]
    #sentences = [s for s in sentences if '?' in s]
    all_qs = len(sentences)

    n = 0
    for i in range(len(sentences)):
        whq = [token.tag_ for token in nlp(sentences[i]) if token.tag_ in tags]

        if len(whq) > 0:
            n += 1

    return all_qs - n, n


def word_start(keywords, doc):
    """
    Find first words in text such as conjunctions and affirmations
    """

    key_res = []
    phrase2_count = []

    # doc = nlp(text)

    for key in keywords:

        first_words = [' ' + prep.prep_simple(str(sent[0])) + ' ' for sent in doc.sents]
        #first_words = [prep.prep_simple(str(fw)) for fw in first_words]
        cs = [w for w in first_words if w in keywords[key]]

        phrase2_count.append(len(cs))
        key_res.append(key)

    res = pd.DataFrame([key_res, phrase2_count], index=['Features', 'Counts']).T
    return res


def adverb_limiter(keywords, doc):
    """
    Search for tokens that are advmod and in the prespecifid list of words
    """

    tags = [token.dep_ for token in doc if token.dep_ == 'advmod' and
            str(' ' + str(token) + ' ') in keywords['Adverb_Limiter']]

    return len(tags)


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

    text = re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r' ', text)
    text = text.lstrip()
    # print(text)
    clean_text = prep.prep_simple(text)
    # print(clean_text)
    doc_text = nlp(text)
    doc_clean_text = nlp(clean_text)

    # quick test to check what's being counted in Positive_Emotion
    # t1 = [token for token in doc_clean_text]
    # print(t1)
    # for t in t1:
    # 	if ' ' + str(t) + ' ' in kw['word_matches']['Positive_Emotion']:
    # 		print(t)

    # Count key words and dependency pairs with negation
    kw_matches = count_matches(kw['word_matches'], doc_text)

    dep_pairs, negations = get_dep_pairs(doc_clean_text)
    dep_pair_matches = count_spacy_matches(kw['spacy_pos'], dep_pairs)

    dep_pairs_noneg = get_dep_pairs_noneg(doc_clean_text)
    disagreement = count_spacy_matches(kw['spacy_noneg'], dep_pairs_noneg)

    neg_dp = set([' ' + i[1] + ' ' for i in negations])
    neg_only = count_spacy_matches(kw['spacy_neg_only'], neg_dp)

    # count start word matches like conjunctions and affirmations
    start_matches = word_start(kw['word_start'], doc_text)

    scores = pd.concat([kw_matches, dep_pair_matches, disagreement, start_matches, neg_only])
    scores = scores.groupby('Features').sum().sort_values(by='Counts', ascending=False)
    scores = scores.reset_index()

    # add remaining features
    bc = bare_command(doc_text)
    scores.loc[len(scores)] = ['Bare_Command', bc]

    ynq, whq = Question(doc_text)

    scores.loc[len(scores)] = ['YesNo_Questions', ynq]
    scores.loc[len(scores)] = ['WH_Questions', whq]

    adl = adverb_limiter(kw['spacy_tokentag'], doc_text)
    scores.loc[len(scores)] = ['Adverb_Limiter', adl]

    scores = scores.sort_values(by='Counts', ascending=False)

    tokens = token_count(doc_text)
    scores.loc[len(scores)] = ['Token_count', tokens]

    return scores


if __name__ == '__main__':

    UPLOAD_FOLDER = '../Data/In/'
    FOLDERS_IN = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']

    text = 'I understand your perspective and agree that I would not want to have resentment in the workplace against women, as that would further compound the issue we are looking at. I do think that it is true that women are underrepresented in STEM careers and am a believer that something should be done to address this discrepancy, even if that is not implementing a priority for women in hiring decisions. While I don\'t think that companies should explicitly hire simply because of their gender, I do think that they should be mindful of the gender gap in STEM and look to address those issues through their hiring practices.'
    # kw is a dictionary of all key words, dependency pairs and negation words
    # print(text)
    kw = keywords.kw
    scores = feat_counts(text, kw)
    print(scores)
