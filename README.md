<b>System for Encouraging Conversational Receptiveness (SECR)<b>

This package consists of 2 main components:
1. Feature parsing
2. Feedback message

Installing and performing feature parsing on local machine

1. In your virtual environment, download requirements.txt
2. To perform feature parsing on a single text, open feature_extraction.py
3. At the bottom of the script, replace the string in line 326 with your own string - make sure to add \n in front of any single quotes in the string

4. To use as part of another script, save a new script
5. In the init.py file, add the name of the new script
6. Import the feature_extraction module: import feature_extraction as fe
7. Import they receptiveness keywords: import keywords
8. Get keywords from keywords.py: kw = keywords.kw
9. To extract features, call the feat_counts function from the feature_extraction module: feat_counts(text, kw)
10. Replace text with your string

Outputs
For feature extraction, a pandas dataframe of Features and feature count is returned.
These counts have not been normalised or scaled

Get feedback messages using local machine

1. Open main_local.py
2. Replace text with your string
3. If deploying as a web service, use main.py rather than main_local.py

Outputs
main.py and main_local.py both return a json output that contains 9 messages ranked in order by the discrepency score (distance between receptiveness feature usage from benchmark usage). The outputs also contain the names of the features after the messages.

