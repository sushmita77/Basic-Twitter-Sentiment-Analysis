# -*- coding: utf-8 -*-


#to interact with twitter use tweepy
import tweepy
import re
#textblob for sentiment analysis
from textblob import TextBlob
from flask import Flask, render_template,request


#create a twitter app and get authentication details from there and insert them for below keys and secret values accordingly

app_consumer_key=	'CONSUMER_KEY'
app_consumer_secret='CONSUMER_SECRET'
app_access_token=	'ACCESS_TOKEN'
app_access_token_secret=	'ACCESS_TOKEN_SECRET'

#authentication process
auth=tweepy.OAuthHandler(app_consumer_key,app_consumer_secret)
auth.set_access_token(app_access_token,app_access_token_secret)
api=tweepy.API(auth)

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])


def index():
	result=None
	ds={ }
	if request.method == 'POST':
		result=request.form['thecontent']   #get the value input from website form
		public_tweet=api.search(result)     #search tweets regarding that word
		
		
		for tweet in public_tweet:
			
			analysis = TextBlob(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))  #tweet.text gives us those sentences found on twitter
			result=analysis.sentiment       #gives the result of polarity
			
			ds[analysis]=result             #store as key:value pair
			#print ds
			
	return render_template('index.html',result=ds)  #return result back to website
			
		
if __name__ == '__main__':
    app.debug = True
    app.run()