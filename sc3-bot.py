#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import time
import tweepy
import random
import datetime
from numpy.random import choice

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user('sc3_bot')

# copied from /usr/share/SuperCollider/HelpSource
elements = ['Classes/', 'Guides/', 'Overviews/', 'Reference/', 'Tutorials/', 'Tutorials/A-Practical-Guide/', 'Tutorials/Getting-Started/', 'Tutorials/JITLib/', 'Tutorials/Mark_Polishook_tutorial/']
weights = [0.821, 0.047, 0.009, 0.042, 0.008, 0.023, 0.016, 0.012, 0.022] # weighted choice based on the number of help files in folders

helpdir = choice(elements, p=weights)
path = "/path/to/bot-data/" + helpdir
helpfile = random.choice(os.listdir(path))

logfile = '/path/to/bot-data/history-sc3-bot.txt'
fn = open(logfile, 'r')
fnlines=fn.readlines()
fn.close()

# Check if helpfile is already posted
for i in fnlines:
    regex = re.compile(helpfile)
    r = re.search(regex, i)
    if r:
        print("Helpfile already posted!")
        helpdir = choice(elements, p=weights)
        path = "/path/to/bot-data/" + helpdir
        helpfile = random.choice(os.listdir(path))

# Write helpfile to log
with open(logfile, "a") as mylog:
    t = datetime.datetime.now()
    mylog.write(helpfile + '\t' + t.strftime("%Y%m%d-%H%M%S"))
    mylog.write("\n")
    mylog.close()

# Open schelp file & read lines to a list
filename = open(path + helpfile,'r')
f = filename.readlines()
filename.close()

# Need improvement
# Assign in myclass the class name
if (helpdir == 'Classes/'):
    myclass = f[0].partition('class::')
    if myclass[2] == '':
        myclass = f[0].partition('CLASS::')
        if myclass[2] == '':
            myclass = f[0].partition('Class::')
else:
    myclass = f[0].partition('title::')
    if myclass[2] == '':
        myclass = f[0].partition('TITLE::')
        if myclass[2] == '':
            myclass = f[0].partition('Title::')
# assign in summary the summary's description
summary = f[1].partition('summary::')
if summary[2] == '':
    summary = f[1].partition('SUMMARY::')
    if summary[2] == '':
        summary = f[1].partition('Summary::')

#print(os.path.splitext(helpfile)[0]) # remove file extension
helpurl = 'http://doc.sccode.org/' + helpdir + os.path.splitext(helpfile)[0] + '.html'

# rstrip removes \s on the right side (summary may have one or two \s)
line = myclass[2].rstrip() + ': ' + summary[2] + helpurl
# post tweet
api.update_status(status=line)
# print tweet in cli
print(line)
# time.sleep(120)#Tweet every 15 minutes

for follower in tweepy.Cursor(api.followers).items():
    try:
        follower.follow()
        print (follower.screen_name)
    except:
        print ('Failed to follow: ', follower.screen_name)
        pass
