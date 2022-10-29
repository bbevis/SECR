#!/usr/bin/env python3
import numpy as np
import pymysql
import cgi
import cgitb
import random
import json
import string
import csv

cgitb.enable()
#############################################################
print("Content-Type: text/html")
print()

db_user = "mikeye5_my"
db_password = "mapleleaf"
db_name = "mikeye5_runone"
db_connection_name = "ace-study-297421:europe-west2:yeomans-database"

unix_socket = '/cloudsql/{}'.format(db_connection_name)
cnx = pymysql.connect(user=db_user, password=db_password,
                      unix_socket=unix_socket, db=db_name)

cr = cnx.cursor()
#############################################################

form = cgi.FieldStorage()
count = form['count'].value

issues={}

if("blm_pos" in form):
	if(form['blm_pos'].value!="4"):
		issues['blm']=form['blm_pos'].value


if("sa_pos" in form):
	if(form['sa_pos'].value!="4"):
		issues['sa']=form['sa_pos'].value

if("stem_pos" in form):
	if(form['stem_pos'].value!="4"):
		issues['stem']=form['stem_pos'].value

if("isis_pos" in form):
	if(form['isis_pos'].value!="4"):
		issues['isis']=form['isis_pos'].value


issuenames=list(issues.items())

random.shuffle(issuenames)

issue=issuenames[0][0]

issue_pos=issuenames[0][1]


if (issue=="blm"):
	issuetext="The public reaction to recent confrontations between police and minority crime suspects has been overblown."

if issue=="sa":
	issuetext="When a sexual assault accusation is made on a college campus, the alleged perpetrator should be immediately removed from campus to protect the well-being of the victim."

if issue=="stem":
	issuetext="In order to increase the representation of women in math, sciences and engineering, female graduates with relevant degrees should be given priority in hiring decisions over men."

if issue=="isis":
	issuetext="The United States should invest greater economic, military, and human resources in fighting the spread of ISIS and similar organizations around the world."


position="pro"
if (int(issue_pos)>4):
	position="anti"

# issue = "stem"
# position = "anti"

dbquery="SELECT * FROM seedTexts WHERE issue='"+issue+"' AND position='"+position+"'"


# Grab all eligibile texts
cr.execute(dbquery)
sqlpull = [list(x) for x in cr.fetchall()]

random.shuffle(sqlpull)

#############################################################
# column ids... ugly, I know
IDcol=0
seedcol=1

spit={}

spit['issue']=issue
spit['issue_pos']=issue_pos
spit['issuetext']=issuetext

for x in range(int(count)):
	theperson=sqlpull[x]
	spit['seedID'+str(x+1)] = theperson[IDcol]
	spit['seedtext'+str(x+1)] = theperson[seedcol]


print(json.dumps(spit))


