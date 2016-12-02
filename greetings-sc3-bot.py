#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

user = api.get_user('sc3_bot')

if(user.followers_count % 100 == 0):
    num = user.followers_count
    line1 = 'Thank you SCers! {0} has now {1} followers!!\n'.format('@sc3_bot', str(num))
    line2 = '{} do: {{ "Robotic thanks!".postln }}'.format(str(num))
    line = line1 + line2
    api.update_status(status=line)
