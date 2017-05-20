#!/usr/bin/python

import pickle
import sys
import os
import random
import re
import time
import requests
from threading import Thread, Lock, Timer
from twython import Twython
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from kim import Kim

SLEEP_TIME = 5
twitter_handle = 'realDonaldTrump'
statusFile = 'status.pickle'
app = Flask('kimagochi')
twitter = None
APP_KEY = os.environ["TWITTER_KEY"]
APP_SECRET = os.environ["TWITTER_SECRET"]
MS_KEY = os.environ["MS_KEY"]
leaders = {}
lastTweetId = 0
token = 0
random.seed()
CORS(app)

def getSentiment(text):
    inp = {'documents': [{'language': 'en', 'id': '1', 'text': text}]}
    headers = {'Ocp-Apim-Subscription-Key': MS_KEY, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    resp = requests.post('https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment', json=inp, headers=headers)
    if resp.status_code == requests.codes.ok:
        return float(resp.json()['documents'][0]['score'])

def mentionsKim(text):
    if re.search("(north korea|kim jong un|democratic people'*s republic of korea|dprk)", text):
        return True
    return False


def updater():
    global twitter, leaders, token, lastTweetId
    while True:
        # TODO:check for tweets
        resp = twitter.show_user(screen_name=twitter_handle)
        if resp != None and resp['status'] != None:
            if resp['status']['id'] != lastTweetId:
                if mentionsKim(resp['status']['text']):
                    sentiment = getSentiment(resp['status']['text'])
                    if sentiment > 0.6:
                        curKim.addPositiveTweet()
                    elif sentiment < 0.4:
                        curKim.addNegativeTweet()
                lastTweetId = resp['status']['id']
        print("leaders: ")
        for kimId in leaders:
            print(kimId)
            curKim = leaders[kimId]
            curKim.nextTick()
        # save data
        dat = {'leaders': leaders,
               'token': token,
               'lastTweetId': lastTweetId}
        with open(statusFile, 'wb') as handle:
            pickle.dump(dat, handle, protocol=pickle.HIGHEST_PROTOCOL)
        time.sleep(SLEEP_TIME)
            


def init():
    global leaders, twitter, token, lastTweetId
    if os.path.isfile(statusFile):
        with open(statusFile, 'rb') as handle:
            data = pickle.load(handle)
            leaders = data['leaders']
            token = data['token']
            lastTweetId = data['lastTweetId']
    if token == 0 or token == None:
        twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
        token = twitter.obtain_access_token() 
    twitter = Twython(APP_KEY, access_token=token)
    Thread(target = updater).start()
    app.run()


@app.route('/create')
def create():
    newId = random.randint(0, 999999)
    while newId in leaders:
        newId = random.randint(0, 999999)
    newKim = Kim(newId)
    leaders[newId] = newKim
    return '{}'.format(newId)

@app.route('/status/<int:kimId>')
def status(kimId):
    print("checking id {}".format(kimId))
    if kimId in leaders:
        kim = leaders[kimId]
        return jsonify(kim.getStatus())
    return 'bad id'

@app.route('/rockets/<int:kimId>')
def rockets(kimId):
    if kimId in leaders:
        kim = leaders[kimId]
        if kim.playWithRockets() == 0:
            return 'success'
        return 'fail' 
    return 'bad id'

@app.route('/parade/<int:kimId>')
def parade(kimId):
    if kimId in leaders:
        kim = leaders[kimId]
        if kim.holdParade() == 0:
            return jsonify(kim.getStatus())
        return 'not enough cash'
        
    return 'bad id'

@app.route('/eat/<int:kimId>')
def eat(kimId):
    if kimId in leaders:
        kim = leaders[kimId]
        kim.eat()
        return jsonify(kim.getStatus())
    return 'bad id'

@app.route('/factory/<int:kimId>')
def factory(kimId):
    if kimId in leaders:
        kim = leaders[kimId]
        kim.visitFactory()
        return jsonify(kim.getStatus()) 
    return 'bad id'


if __name__ == '__main__':
    init()
