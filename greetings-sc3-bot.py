#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user('sc3_bot')

if(user.followers_count % 100 == 0):
    num = user.followers_count
    line1 = 'Thank you SCers! {0} has now {1} followers!!\n'.format('@sc3_bot', str(num))
    line2 = '{} do: {{ "Robotic thanks!".postln }}'.format(str(num))
    line = line1 + line2
    api.update_status(status=line)

if (user.followers_count == 140):
    line = ''
    for i in range(0,user.followers_count):
        line = '@' + line
    api.update_status(status=line)
