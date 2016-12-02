#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os import listdir
from os.path import isfile, join
import re
import tweepy
import random
import datetime
from numpy.random import choice
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

user = api.get_user('sc3_bot')

# copied from /usr/share/SuperCollider/HelpSource
elements = ['Classes/', 'Guides/', 'Overviews/', 'Reference/', 'Tutorials/', 'Tutorials/A-Practical-Guide/', 'Tutorials/Getting-Started/', 'Tutorials/JITLib/', 'Tutorials/Mark_Polishook_tutorial/']
weights = [0.821, 0.047, 0.009, 0.042, 0.008, 0.023, 0.016, 0.012, 0.022] # weighted choice based on the number of help files in folders

# read log
datapath = '/home/aucotsi/github/sc3_bot_twitter/bot-data/'
logfile = datapath + 'history-sc3-bot.txt'
fn = open(logfile, 'r')
fnlines=fn.readlines()
fn.close()

# chose a dir path and a file to read
helpdir = choice(elements, p=weights)
path = datapath + helpdir
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
helpfile = choice(onlyfiles)

# Check in logfile if helpfile is already posted
s = ""
for i in fnlines:
    s += str(i)
    cnt = 0
    running = True
    while running:
        r = re.search(helpfile, s)
        if r:
            cnt += 1
            helpdir = choice(elements, p=weights)
            path = datapath + helpdir
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            helpfile = choice(onlyfiles)
        else:
            running = False

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

# Assign in myclass the class name
# assign in mysummary the summary's description
for readlines in f:
    # match class or title
    match_title = re.match('(class|title)::\s*([A-Za-z0-9+-/\_\"\']*\s)*', readlines, flags=re.IGNORECASE)
    if match_title:
        classOrTitle = re.split('::', match_title.group(), flags=re.IGNORECASE)
        myclass = classOrTitle[1]
    # match summary
    match_summary = re.match('summary::\s*([a-z0-9+-/\_\"\'\.]*:?\s)*', readlines, flags=re.IGNORECASE)
    if match_summary:
        summary = re.split('::', match_summary.group(), flags=re.IGNORECASE)
        mysummary = summary[1]

#print(os.path.splitext(helpfile)[0]) # remove file extension
helpurl = 'http://doc.sccode.org/' + helpdir + os.path.splitext(helpfile)[0] + '.html'

# rstrip removes \n on the right side
line = myclass.rstrip() + ': ' + mysummary + helpurl
# post tweet with helpfile
api.update_status(status=line)

# matching and printing a ugen tweet
myugens = list()
for readlines in f:
    match_category  = re.match('categories::\s*ugens(>*A-Z)*', readlines, flags=re.IGNORECASE)
    if match_category:
        print(match_category.group())
        for currline in f:
            match_ugen  = re.match('\{(.*?)\}\.(play);?', currline)
            if match_ugen:
                # append lines smaller than 140 chars
                if len(match_ugen.group())<133:
                    myugens.append(match_ugen.group())

if len(myugens) > 0:
    ugentweet = max(myugens, key=len) + '//#sc140'
    api.update_status(status=ugentweet) # post sc140 tweet
    #print(ugentweet)

# print tweet in cli
print(line)

followers = api.followers_ids()
friends = api.friends_ids()
# unfollow non-followers
for i in friends:
    if i not in followers:
        try:
            api.destroy_friendship(i)
        except:
            pass

# follow back followers
for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
