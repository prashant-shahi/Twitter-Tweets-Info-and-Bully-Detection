#!/usr/bin/python

import string
import sys
import re

table = str.maketrans("", "", string.punctuation)
numberoftimes = 0

if len (sys.argv) > 1:
	try:
		numberoftimes = int(sys.argv[1])
	except ValueError:
		print("Argument not a number\nUsage: python3 badwords.py custom_number(1 to 25s)")
		exit()

	numberoftimes = int(sys.argv[1])
	if(numberoftimes>15):	# Limiting because of the limit of 450 requests per 15 minutes
		numberoftimes = 15
	print("Tweets count: " + str(numberoftimes))
else:
	numberoftimes = 1
	print("Default tweet count: 1\nFor custom number(1 to 25) of tweets:\nUsage: python3 badwords.py custom_number")

print("Comparing with " + str(numberoftimes) + " number of tweet(s)")

badwords = []
for line in open("badwords.txt"):
	for word in line.split( ):
		badwords.append(word)

import tweepy
from tweepy import OAuthHandler


# @ http://developer.twitter.com - Register and obtain api keys and set it up

consumer_key = "HxfKO5bmkLa5wk1mWXJO1Yt0M"  # consumer key for twitter application
consumer_secret = "ivunoaSl7hsaxdrGd5XsI2JPhBoikOMHHswCVuMGSL5wEtwWWG"  # secret consumer key for twitter application
access_token = "999771859326398464-WOxjpZ7rB0YmrWfJebgmz9fGRVAm70V"   # access token for test bot account
access_secret = "uQsyWghDqewBm0hyI4SQbZ53y4i42RiVH8mABHWu4qwaC"   # secret access token for test bot account


# set up auth and api
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# print ("type: {0}\nValue = {1}".format(type(numberoftimes),numberoftimes))

count = 1

for status in tweepy.Cursor(api.home_timeline).items(numberoftimes):
	print ("\n\n{0}. Tweet:\t {1}".format(count,status.text))

	# get rid of punctuation
	tweet = status.text
	tweet = "".join(l for l in tweet if l not in string.punctuation)
	tweet = tweet.lower()
	bullying = False
	for word in tweet.split(" "):
		word = word.translate(table)
		if word in badwords:
			bullying = True
			break;

	if bullying == True:
		print("Status: Bullying\tRetweet: {0}\tFavourite: {1}\tUser: @{2} ({3})\tFollowers: {4}".format(status.retweet_count,status.favorite_count,status.author.screen_name,status.author.name,status.user.followers_count))
	if bullying == False:
		print("Status: Not Bullying\tRetweet: {0}\tFavourite: {1}\tUser: @{2} ({3})\tFollowers: {4}".format(status.retweet_count,status.favorite_count,status.author.screen_name,status.author.name,status.user.followers_count))

	count = count+1