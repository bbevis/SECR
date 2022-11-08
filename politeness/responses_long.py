fancy_responses = {
    'Agreement':
    {'fancy_name': 'Agreement phrases',
     'recog': '<p>You <b>used enough</b> agreement phrases (e.g. <q>I agree</q>, <q>you are right</q>). <b>Keep using these phrases</b> next time! Even when you passionately disagree with someone, they usually have some shared values or common ground. Highlighting areas of agreement, no matter how small or obvious, helps to build an environment of constructive debate.</p>',
     'imp': '<p>You <b>could use more</b> agreement phrases (e.g. <q>I agree</q>, <q>you are right</q>). <b>Use more of these phrases</b> next time! Even when you passionately disagree with someone, they usually have some shared values or common ground. Highlighting areas of agreement, no matter how small or obvious, helps to build an environment of constructive debate.</p>'},

        'Positive_Emotion':
    {'fancy_name': 'Positive emotion phrases',
     'recog': '<p>You <b>used enough</b> positive emotion words (e.g. <q>good</q>, <q>happy</q>). <b>Keep using these words</b> next time and continue phrasing your arguments in a positive way. This will help you avoid the appearance of contradicting the beliefs of others. </p>',
     'imp': '<p>You <b>could use more</b> positive emotion words (e.g. <q>good</q>, <q>happy</q>). <b>Use more of these words</b> next time! Phrasing your arguments in a positive way. This will help you avoid the appearance of contradicting the beliefs of others. </p>'},

        'Reasoning':
    {'fancy_name': 'Reasoning words',
     'imp': '<p>You used <b>too many</b> reasoning phrases (e.g. <q>therefore</q>, <q>because</q>). Try to <b>decrease this</b> next time! Words such as <q>therefore</q> and <q>because</q> can sound condescending when used too many times.</p>',
     'recog': '<p>You <b>avoided</b> reasoning phrases (e.g. <q>therefore</q>, <q>because</q>). Keep <b>avoiding</b> these phrases! Words such as <q>therefore</q> and <q>because</q> can sound condescending when used too many times.</p>'},

        'Subjectivity':
    {'fancy_name': 'Subjective phrases',
     'recog': '<p>Subjective phrases help to make your arguments seem less direct in opposition. Being less direct signals your intention to engage in a debate rather than to fight. The algorithm noticed you <b>used enough</b> subjective phrases (e.g. <q>I believe</q> or <q>In my opinion</q>). <b>Keep using these phrases</b> next time!</p>',
     'imp': '<p>Subjective phrases help to make your arguments seem less direct in opposition. Being less direct signals your intention to engage in a debate rather than to fight. The algorithm noticed you <b>could use more</b> subjective phrases (e.g. <q>I believe</q> or <q>In my opinion</q>). <b>Use more of these phrases</b> next time!</p>'},

        'Acknowledgement':
    {'fancy_name': 'Acknowledgement phrases',
     'recog': '<p>You <b>used enough</b> acknowledgement phrases (e.g. <q>I understand</q> or <q>I get</q>). <b>Keep using these phrases</b> next time! Actively acknowledging that other opinions are valid, even if you do not agree with them, signals that you listen. This in turn encourages others to listen to your opinions.</p>',
     'imp': '<p>You <b>could use more</b> acknowledgement phrases (e.g. <q>I understand</q> or <q>I get</q>). <b>Use more of these phrases</b> next time! Actively acknowledging that other opinions are valid, even if you do not agree with them, signals that you listen. This in turn encourages others to listen to your opinions.</p>'},

        'Negation':
    {'fancy_name': 'Negation words',
     'imp': '<p>You used <b>too many</b> negation words (e.g. <q>did not</q>, <q>would not</q>). Try to <b>decrease this</b> next time! Phrasing your arguments in positive terms helps avoid appearing argumentative - even if your opinions contradtict. This increases the chances of a more open response in return.</p>',
     'recog': '<p>You <b>avoided</b> negation words (e.g. <q>did not</q>, <q>would not</q>). Keep <b>avoiding</b> these phrases!Phrasing your arguments in positive terms helps avoid appearing argumentative - even if your opinions contradtict. This increases the chances of a more open response in return.</p>'},

        'Hedges':
    {'fancy_name': 'Hedging words',
     'recog': '<p>You <b>used enough</b> hedging words (e.g. <q>almost</q> or <q>maybe</q>). <b>Keep using these words</b> next time! Hedging your claims signals that you are open to other viewpoints. In return, others will be more open to yours.</p>',
     'imp': '<p>You <b>could use more</b> hedging words (e.g. <q>almost</q> or <q>maybe</q>). <b>Use more of these words</b> next time! Hedging your claims signals that you are open to other viewpoints. In return, others will be more open to yours.</p>'},

        'Second_Person':
    {'fancy_name': 'Second person words',
     'recog': '<p>The algorithm noticed you <b>used enough</b> second person phrases (e.g. <q>you</q> or <q>yourself</q>). <b>Keep using these phrases</b> next time!</p>',
     'imp': '<p>The algorithm noticed <b>could use more</b> second person phrases (e.g. <q>you</q> or <q>yourself</q>). <b>Use more of these phrases</b> next time!</p>'},

        'Adverb_Limiter':
    {'fancy_name': 'Words that limit a statement',
     'imp': '<p>You used <b>too many</b> adverb limiters (e.g. <q>just</q>, <q>only</q>). Try to <b>decrease this</b> next time! It is tempting to offer explanations for your opposing viewpoint but be mindful that words such as <q>just</q> and <q>only</q> can sound condescending when you explain your viewpoint. Suggesting that things are obvious makes people feel inferior.</p>',
     'recog': '<p>You <b>avoided</b> adverb limiters (e.g. <q>just</q>, <q>only</q>). Keep <b>avoiding</b> these phrases! It is tempting to offer explanations for your opposing viewpoint but be mindful that words such as <q>just</q> and <q>only</q> can sound condescending when you explain your viewpoint. Suggesting that things are obvious makes people feel inferior.</p>'},

        'Disagreement':
    {'fancy_name': 'Disagreement phrases',
     'imp': '<p>You used <b>too many</b> disagreement phrases (e.g. <q>I disagree</q>, <q>You are wrong</q>). Try to <b>decrease this</b> next time! Even when you passionately disagree with someone, they usually have some shared values or common ground. Highlighting areas of agreement, no matter how small or obvious, helps to build an environment of constructive debate.</p>',
     'recog': '<p>You <b>avoided</b> disagreement phrases (e.g. <q>I disagree</q>, <q>You are wrong</q>). Keep <b>avoiding</b> these phrases! Even when you passionately disagree with someone, they usually have some shared values or common ground. Highlighting areas of agreement, no matter how small or obvious, helps to build an environment of constructive debate.</p>'},

    'Negative_Emotion':
    {'fancy_name': 'Negative emotion phrases',
     'imp': '<p>You used <b>too many</b> negative emotion phrases (e.g. <q>You are hopeless</q>, <q>This is not feasible</q>). Try to <b>decrease this</b> next time! Phrases that contain negative emotions would make others less likely to want to engage with you.</p>',
     'recog': '<p>You <b>avoided</b> negative emotion phrases (e.g. <q>You are hopeless</q>, <q>This is not feasible</q>). Keep <b>avoiding</b> these phrases! Phrases that contain negative emotions would make others less likely to want to engage with you.</p>'}
}

"""
fancy_responses = {
   'WH_Questions': {'fancy_name': 'question words', 'imp': 'such as how, why and where?'},
   'Bare_Command': {'fancy_name': 'soft commands', 'imp': 'such as consider'},
   'Conjunction_Start': {'fancy_name': 'conjunctions at the beginning of the sentence', 'imp': 'such as but, and, then'},
   'Affirmation': {'fancy_name': 'affirmative words', 'imp': 'such as for you'},
   'For_You': {'fancy_name': 'phrases that shows consideration to the other person', 'imp': 'such as for you...'},
   'Swearing': {'fancy_name': 'swear words', 'imp': ''},
   'Formal_Title': {'fancy_name': 'be more formal', 'imp': 'by using formal titles'},
   'For_Me': {'fancy_name': 'phrases that show nuanced opinions', 'imp': 'such as for me...'},
   'Informal_Title': {'fancy_name': 'informal titles', 'imp': 'by using informal titles such as dude, buddy'},
   'Agreement': {'fancy_name': 'agreement phrases', 'imp': 'such as I agree and you are right'},
   'Disagreement': {'fancy_name': 'disagreement phrases', 'imp': 'such as I disagree or You are wrong'},
   'Give_Agency': {'fancy_name': 'giving phrases', 'imp': 'such as let you or you may'},
   'Could_You': {'fancy_name': 'ask formally', 'imp': 'such as could you or would you'},
   'Gratitude': {'fancy_name': 'gratitude', 'imp': 'such as thanks'},
   'Positive_Emotion': {'fancy_name': 'positive emotions', 'imp': 'such as adore or happy'},
   'Reasoning': {'fancy_name': 'reasoning words', 'imp': 'such as because or explain'},
   'Subjectivity': {'fancy_name': 'subjective phrases', 'imp': 'such as I believe or In my opinion'},
   'Acknowledgement': {'fancy_name': 'acknowledgement phrases', 'imp': 'such as I understand or I get'},
   'Negative_Emotion': {'fancy_name': 'negative emotions', 'imp': 'such as absurd or ignorant'},
   'Negation': {'fancy_name': 'fewer negation words', 'imp': 'such as did not or will not'},
   'Hedges': {'fancy_name': 'hedging words', 'imp': 'such as almost or maybe'},
   'Impersonal_Pronoun': {'fancy_name': 'impersonal pronouns', 'imp': 'such as others or someone'},
   'Filler_Pause': {'fancy_name': 'filler pauses', 'imp': 'such as um and hm'},
   'By_The_Way': {'fancy_name': 'the phrase by the way', 'imp': ''},
   'Reassurance': {'fancy_name': 'reassuring words', 'imp': 'such as it\'s ok or don\'t worry'},
   'Hello': {'fancy_name': 'greeting phrases', 'imp': 'such as hello or hi'},
   'Please': {'fancy_name': 'polite requests', 'imp': 'such as please'},
   'First_Person_Plural': {'fancy_name': 'first person phrases', 'imp': 'such as us and our'},
   'First_Person_Single': {'fancy_name': 'first person phrases', 'imp': 'such as myself or I'},
   'Second_Person': {'fancy_name': 'second person phrases', 'imp': 'such as you or yourself'},
   'Apology': {'fancy_name': 'apologetic tones', 'imp': 'such as excuse me or forgive me'},
   'Truth_Intensifier': {'fancy_name': 'words that intensify a statement', 'imp': 'such as really or surely'},
   'Can_You': {'fancy_name': 'ask formally', 'imp': 'such as can you or will you'},
   'Let_Me_Know': {'fancy_name': 'the phrase let me know', 'imp': ''},
   'Goodbye': {'fancy_name': 'farewell phrases', 'imp': 'such as goodbye or see you later'},
   'Ask_Agency': {'fancy_name': 'ask agencies', 'imp': 'such as do me a favour or might I'},
   'YesNo_Questions': {'fancy_name': 'yes or no questions', 'imp': 'as opposed to who, where, what, and why questions'},
   'Adverb_Limiter': {'fancy_name': 'words that limit a statement', 'imp': 'such as just or only'},
   }
   """
