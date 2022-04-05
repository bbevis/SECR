import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import en_core_web_sm
nlp = en_core_web_sm.load()
nlp.enable_pipe("senter")

import feature_extraction as fe
import prep
import keywords


UPLOAD_FOLDER = '../Data/'
filename = 'responses by cond.csv'
kw = keywords.kw
main_features = ['Acknowledgement', 'Agreement', 'Hedges', 'Negation', 'Positive_Emotion', 'Reasoning', 'Subjectivity', 'Adverb_Limiter', 'Second_Person']
main_features_sort = sorted(main_features)

#r0 = responses[0]


def load(n):

    if n is not None:
        responses = pd.read_csv(UPLOAD_FOLDER + filename).iloc[:n]
    else:
        responses = pd.read_csv(UPLOAD_FOLDER + filename)

    # remove nan
    responses = responses.dropna()

    cond = responses['Group'].tolist()
    responses = responses['response'].tolist()
    
    return responses, cond

def sent_split(sentences, l_sent_ls):

    l_sent_ls.append(len(sentences))

    return l_sent_ls

def token_count(sentences):

    n_tokens_ls = []

    for s in sentences:

        text = re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r' ', s)
        text = text.lstrip()
        text = prep.prep_simple(text)

        doc_text = nlp(text)

        count = fe.token_count(doc_text)
        n_tokens_ls.append(count)

    return n_tokens_ls

def feat_counts_sent(sentences):

    scores_ls = []

    for s in sentences:

        scores = fe.feat_counts(s, kw)
        scores = scores[scores['Features'].isin(main_features)].sort_values(by='Features')['Counts'].to_list()
        scores_ls.append(scores)

    return scores_ls

def ave_middle(x):

    # Remove first and last value then average the remainder

    x = x[1:]
    x = np.array(x[:-1])
    x = np.average(x, axis=0).tolist()

    return x


def sent_level_feats(n=None):

    responses, cond = load(n)

    scores_sent_first_all = []
    scores_sent_last_all = []
    scores_sent_middle_all = []

    l_sent_ls = []

    res = pd.DataFrame()

    for i in range(len(responses)):

        r = responses[i]
        sentences = prep.sentenciser(r)

        # For initial analysis, use responses with 3 or more sentences long
        if len(sentences) > 2 and len(sentences) < 5:

            #l_sent_ls = sent_split(sentences, l_sent_ls)
            n_tokens_ls = token_count(sentences)

            scores_ls = feat_counts_sent(sentences)

            scores_sent_middle = ave_middle(scores_ls)
            token_sent_middle = ave_middle(n_tokens_ls)

            # create df for feature counts and token counts.
            df = pd.DataFrame({
                'Condition': cond[i],
                'Features': main_features_sort,
                'First sentence': scores_ls[0],
                'Middle sentence': scores_sent_middle,
                'Last sentence': scores_ls[-1],
                'Token count first': n_tokens_ls[0],
                'Token count middle': token_sent_middle,
                'Token count last': n_tokens_ls[-1],
                'Response text': r
                })

            # normalising for number of tokens
            df['First sentence normalised'] = df['First sentence'] / df['Token count first'] * 100
            df['Middle sentence normalised'] = df['Middle sentence'] / df['Token count middle'] * 100
            df['Last sentence normalised'] = df['Last sentence'] / df['Token count last'] * 100

            res = res.append(df)

    return res

def plot_sentence_dist(x, title, ylab, xlab, outfile):

    plt.hist(x, bins=range(int(min(x)), int(max(x)) + 1, 1), rwidth=0.9, align='left')
    plt.title(title)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.savefig(outfile, dpi=300)
    plt.clf()

def create_subplot(f, ax, feature_name, sent_order, df, x_lab, y_lab, facecolor, color, fontsize):

    """
    Creates one subplot of a histogram distribution of feature count and title
    """

    x = df[sent_order][df['Feature'] == feature_name]

    ax.hist(x, facecolor=facecolor, bins = range(int(min(x)), int(max(x)) + 1, 1), rwidth=0.9, align = 'left')
    ax.set(xticks = range(int(min(x)), int(max(x)) + 1, 1), xlim=[- 1, max(x)])
    ax.set_title(feature_name +  '\nthreshold: '
        + str(thresholds[f]), size = 12)
    ax.set_xlabel(x_lab, fontsize = fontsize)
    ax.set_ylabel(y_lab, fontsize = fontsize)
    ax.tick_params(labelsize= fontsize)
    ax.patch.set_facecolor('whitesmoke')

def feat_dist(df, x_lab, y_lab, facecolor, color, fontsize):

    fig = plt.figure(figsize=(9, 10))
    fig.suptitle('Usage per 100 words')

    for f in range(len(main_features)):
        ax = fig.add_subplot(3, 3, f + 1)
        create_subplot(f, ax, main_features[f], df, x_lab, y_lab, facecolor, color, fontsize)

    fig.subplots_adjust(wspace=0.5)
    fig.subplots_adjust(hspace=0.7)
    # plt.show()
    fig.savefig('../Out/Images/sent feat dist.png', dpi = 300)


res = sent_level_feats()
res.to_csv('../Out/sent comp analysis.csv', index=False)

# feat_dist(res, 'Feature counts', 'Count of responses', 'darkblue', 'darkmagenta', 10)


# ave_tokens = sum(n_tokens_ls) / sum(l_sent_ls)
# print(ave_tokens)


# plot_sentence_dist(l_sent_ls, "Distribution of sentence counts", "Frequency", "Count of sentences", "../Out/Images/dist_sentence_counts.png")
# plot_sentence_dist(n_tokens_ls, "Distribution of tokens counts", "Frequency", "Count of tokens", "../Out/Images/dist_token_counts.png")

# l_sent_ls = [x for x in l_sent_ls if x <= 10]
# plot_sentence_dist(l_sent_ls, "Distribution of sentence counts", "Frequency", "Count of sentences", "../Out/Images/dist_sentence_counts_cut.png")
