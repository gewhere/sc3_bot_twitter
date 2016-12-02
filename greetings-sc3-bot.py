#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy

consumer_key = "xvLbp1IHt22JvE0eQRGwYNNWD"
consumer_secret = "MtEhytllKGYOmeGynT75uPd0JXmvjIoOMh3c7z6t1hqfHnJLEj"
access_token = "803612839114117120-mduc3Thn5kR2qaEQ5q5Gj6SozcCzz4F"
access_token_secret = "Xn6Gz5Pduy9kITaGE3qfaQ4fun5dOPd9Rfks45AYCe0O4"

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
