import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class TwitterHeatMap():
    
    def __init__(self, user):
        self.headers = {'Authorization': 'Bearer <ADD BEARER KEY HERE>'}
        self.user = user
        self.tweetList = self.listOfTweets()
        self.tweets = self.tweetsPerDay(self.tweetList)
        self.buildHeatMap(self.tweets)
        
    def getTweetsList(self):
        return self.tweets
        
    def getTweets(self):
        url = 'https://api.twitter.com/2/tweets/search/recent?query=from:' + self.user
        r  = requests.get(url=url, headers=self.headers)
        data = r.json()
        return data

    def listOfTweets(self):
        tweets = self.getTweets()
        
        if tweets['meta']['result_count'] >= 1:
            tweets = tweets['data']
        else:
            tweets = []
            
        tweetList = []
        #print(tweets)
        for tweet in tweets:
            
            ID = tweet['id']
            url = 'https://api.twitter.com/1.1/statuses/show.json?id='+ ID
            r  = requests.get(url=url, headers=self.headers)
            data = r.json()
            tweetList.append(data)
            
        return tweetList
    
    def tweetsPerDay(self, tweetList):
        daysOfWeek = {'Mo':0,'Tu':0,'We':0,'Th':0,'Fr':0,'Sa':0,'Su':0}
        for tweet in tweetList:
            daysOfWeek[tweet['created_at'][:2]] += 1
    
        return daysOfWeek

        
    def buildHeatMap(self, daysOfWeek):
        
        x = [daysOfWeek['Su'],
         daysOfWeek['Mo'],
         daysOfWeek['Tu'],
         daysOfWeek['We'],
         daysOfWeek['Th'],
         daysOfWeek['Fr'],
         daysOfWeek['Sa']]

        x = np.array(x)
        x_res=x.reshape(1, 7)
        
        positions = range(1, 8)
        labels = ("Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat")

        fig, ax = plt.subplots(figsize=(7,4))
        sns.heatmap(x_res, square=False, ax=ax, cmap="Reds")
        plt.yticks(rotation=10,fontsize=8)
        plt.xticks(positions, labels=labels, fontsize=12)
        plt.savefig(self.user+'_heat_map.png')
        plt.show()
        

