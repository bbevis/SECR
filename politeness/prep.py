import os
import regex
import re
import pickle
import en_core_web_sm
nlp = en_core_web_sm.load()
# nlp.enable_pipe("senter")

#import nltk
#from nltk.corpus import stopwords
#from nltk import tokenize

#from textblob import TextBlob

#import spacy

def load_to_lists(path, words):

    keywords = []

    all_files = os.listdir(path)

    all_files = [file for file in all_files if file.endswith(".txt")]
    all_filenames = [file.split('.', 1)[0] for file in all_files if file.endswith(".txt")]

    feature_names = []

    all_lines = []
    for i in range(len(all_files)):

        if all_files[i].endswith(".txt"):
            try:
                with open(os.path.join(path, all_files[i]), "r") as f:
                    for line in f:
                        splitLine = line.split()

                        if words == 'single':
                            splitLine = ' '.join(splitLine)
                            splitLine = [splitLine.center(len(splitLine) + 2)]
                            all_lines.extend(splitLine)

                        if words == 'multiple':
                            all_lines.append(splitLine)

                        feature_names.append(all_filenames[i])

                # print(keywords[all_filenames[i]])
            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise

    return feature_names, all_lines

# def load_data(paths, words_in_line):

# 	all_names = []
# 	all_attributes = []
# 	for i in range(len(paths)):
# 		names, attributes = load_to_lists(paths[i], words = words_in_line[i])
# 		all_names.extend(names)
# 		all_attributes.extend(attributes)


# 	return all_names, all_attributes


def load_to_dict(path, words):
    """
    Main function for taking raw .txt files and generates a python dictionary
    Used in conjunction with committ_data function
    """

    keywords = {}

    all_files = os.listdir(path)

    all_files = [file for file in all_files if file.endswith(".txt")]
    all_filenames = [file.split('.', 1)[0] for file in all_files if file.endswith(".txt")]

    for i in range(len(all_files)):
        all_lines = []
        if all_files[i].endswith(".txt"):
            try:
                with open(os.path.join(path, all_files[i]), "r") as f:
                    for line in f:
                        splitLine = line.split()

                        if words == 'single':
                            splitLine = [' '.join(splitLine)]
                            all_lines.extend(splitLine)

                        if words == 'multiple':
                            #splitLine = multi_strings(line)
                            all_lines.append(splitLine)

                if words == 'single':
                    all_lines = [l.center(len(l) + 2) for l in all_lines]

                keywords[all_filenames[i]] = all_lines
                # print(keywords[all_filenames[i]])
            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise

    return keywords


def commit_data(path, path_in, folders, words_in_line):
    """
    Loads data from .txt files, creates one dictionary per folder
    and outputs each folder as a dictionary in a pickle file
    """

    for i in range(len(folders)):
        x = load_to_dict(path + folders[i], words_in_line[i])

        file = open(path_in + folders[i] + ".pkl", "wb")
        pickle.dump(x, file)
        file.close()


def load_saved_data(path_in, folders):
    """
    Loads predefined keywords and dependency pairs

    Input:
            Pickle files of dictionaries saved in directory

    Output:
            Python dictionaries
    """

    dicts = {}

    for i in range(len(folders)):

        file = open(path_in + folders[i] + ".pkl", "rb")
        x = pickle.load(file)
        dicts[folders[i]] = x
        file.close()

    return dicts

def clean_text(text):

    orig = ["let's", "i'm", "won't", "can't", "shan't", "'d",
            "'ve", "'s", "'ll", "'re", "n't", "u.s.a.", "u.s.", "e.g.", "i.e.",
            "‘", "’", "“", "”", "100%", "  ", "mr.", "mrs."]

    new = ["let us", "i am", "will not", "cannot", "shall not", " would",
           " have", " is", " will", " are", " not", "usa", "usa", "eg", "ie",
           "'", "'", '"', '"', "definitely", " ", "mr", "mrs"]

    for i in range(len(orig)):
        text = text.replace(orig[i], new[i])

    return text

def prep_simple(text):

    # text cleaning

    t = text.lower()
    t = clean_text(t)
    t = re.sub(r"[.?!]+\ *", "", t)  # spcifially replace punctuations with nothing
    t = re.sub('[^A-Za-z,]', ' ', t)  # all other special chracters are replaced with blanks

    return t

def prep_whole(text):

    t = text.lower()
    t = clean_text(t)
    t = re.sub('[^A-Za-z]', ' ', t)

    words = nltk.word_tokenize(t)

    stopword = set(stopwords.words('english'))
    words = [w for w in words if not w in stopword]
    text = ' '.join(words)

    return text


def sentenciser(text):

    #nlp = spacy.load("en_core_web_sm", exclude=["parser"])
    nlp.enable_pipe("senter")

    doc = nlp(text)

    split_t = [sent.text for sent in doc.sents]

    return split_t

def punctuation_seperator(text):

    #x = tokenize.sent_tokenize(self.text)

    # split string by punctuation
    PUNCT_RE = regex.compile(r'(\p{Punctuation})')
    split_punct = PUNCT_RE.split(text)
    # print(split_punct)

    # Removing punctuation from the list
    no_punct = []
    for s in split_punct:
        s = re.sub(r'[^\w\s]', '', s)
        if s != '':
            no_punct.append(s)

    return no_punct

def conjection_seperator(text):

    tags = nltk.pos_tag(nltk.word_tokenize(text))

    # print(tags)

    first_elements = [e[0] for e in tags]
    second_elements = [e[1] for e in tags]

    if 'CC' in second_elements:
        index = [i for i, e in enumerate(second_elements) if e == 'CC']
        index.insert(0, 0)
        parts = [first_elements[i:j] for i, j in zip(index, index[1:] + [None])]

        return [' '.join(p) for p in parts]
    else:
        return [' '.join(first_elements)]

def phrase_split(text):

    text = punctuation_seperator(text)

    # print(text)

    phrases = []
    for t in text:
        t = conjection_seperator(t)

        phrases.extend(t)

    return phrases


if __name__ == '__main__':

    #text = "I'm not quite sure how you understand, please could you let me know how you came to this way of thinking? Would you mind?"
    # text = "Hello, how are you, Do you like breakfast? Baked beans really smell. Kittens love to play. Let's do some work"
    # text = sentenciser(text)
    # text = [prep_simple(t) for t in text]
    # print(text)

    PATH = '../Data/'
    UPLOAD_FOLDER = '../Data/In/'
    FOLDERS_IN = ['word_matches', 'spacy_pos', 'spacy_noneg', 'spacy_neg_only', 'word_start', 'spacy_tokentag']
    READ_TYPE = ['single', 'multiple', 'multiple', 'single', 'single', 'single']

    commit_data(PATH, UPLOAD_FOLDER, FOLDERS_IN, READ_TYPE)
