import random

GAMESPEED = 1

conf = {'hungerTicks': 15,
        'boredomTicks': 30,
        'penaltyTicks': 5,
        'paradeCost': 300,
        'paradeBoost': 40,
        'rocketHappinessBoost': 40,
        'rocketPrestigeBoost': 5,
        'rocketBoredomBigBoost': 25,
        'rocketBoredomSmallBoost': 10,
        'rocketFail': 15,
        'eatBoost': 15,
        'factoryBoost': 5,
        'boredomPenalty': 3,
        'hungerPenalty': 2,
        'prestigePenalty': 5,
        'eventProb': 50,
        'eventLimit': 20}


events = [{'description': "The Chinese government has given you foregin aid to relieve the food shortage in Democratic People's Republic of Korea. +175 cash",
           'hunger': 0,
           'happiness': 0,
           'boredom': 0,
           'prestige': 0,
           'cash': 175},
           {'description': 'It turns out that the South Korean president was controlled by a witch. You are entertained by their weakness! +5 happiness, -15 boredom',
           'hunger': 0,
           'happiness': 5,
           'boredom': -15,
           'prestige': 0,
           'cash': 0},
           {'description': 'Your uncle was starting to challenge your power. Because there can only be one supreme leader, you have him executed. -10 prestige, -30 cash',
           'hunger': 0,
           'happiness': 0,
           'boredom': 0,
           'prestige': -10,
           'cash': -30},
           {'description': "A dissident speaks lies about the glorious Democratic People's Republic of Korea at the United Nations. -15 prestige",
           'hunger': 0,
           'happiness': 0,
           'boredom': 0,
           'prestige': -15,
           'cash': 0},
           {'description': 'Our scientist have scientificly proven that our burgers are superior to American burgers! You celebrate by eating 20! -20 hunger',
           'hunger': -20,
           'happiness': 0,
           'boredom': 0,
           'prestige': 0,
           'cash': 0},
           {'description': 'An American college student tried to steal a poster of you. We imprisoned him for this vile act! +20 prestige, -10 boredom',
           'hunger': 0,
           'happiness': 0,
           'boredom': -10,
           'prestige': 20,
           'cash': 0}]

class Kim(object):
    
    def __init__(self, name):
        self.name = name
        self.hunger =  50
        self.happiness = 100
        self.boredom = 20
        self.prestige = 51
        self.cash = 0
        self.ticks = 0
        self.events = []

    def addEvent(self, description):
        self.events.append(description)
        if len(self.events) > conf['eventLimit']:
            self.events.pop(0) 

    def triggerEvent(self):
        event = random.choice(events)
        self.addEvent(event['description']) 
        self.hunger += event['hunger']
        self.happiness += event['happiness']
        self.boredom += event['boredom']
        self.prestige += event['prestige']
        self.cash += event['cash']
        self.checkBounds()

    def addPositiveTweet(self):
        self.addEvent('The American leader Trump has praised you! Long live the Supreme Leader! happiness +50!')
        self.happiness += 50
        self.checkBounds()

    def addNegativeTweet(self):
        self.addEvent('The American leader Trump has insulted our glorious nation! happiness -30!')
        self.happiness -= 30
        self.checkBounds()


    def nextTick(self):
        self.ticks += GAMESPEED
        if self.ticks % conf['hungerTicks'] == 0 and self.hunger < 100:
            self.hunger += 1
        if self.ticks % conf['boredomTicks'] == 0 and self.boredom < 100:
            self.boredom += 1
        if self.boredom == 100 and self.ticks % conf['penaltyTicks']:
            self.happiness -= conf['boredomPenalty']
        if self.hunger == 100 and self.ticks % conf['penaltyTicks']:
            self.happiness -= conf['hungerPenalty']
        if self.prestige == 0 and self.ticks % conf['penaltyTicks']:
            self.happiness -= conf['prestigePenalty']

        if random.randint(1, conf['eventProb']) == 1:
            self.triggerEvent()
            return 1
        return 0

    def eat(self):
        self.hunger += conf['eatBoost']
        self.checkBounds()

    def visitFactory(self):
        self.boredom += conf['factoryBoost']
        self.checkBounds()

    def playWithRockets(self):
        if random.randint(0, 4) >= 4: 
            # success
            self.happiness += conf['rocketHappinessBoost']
            self.boredom -= conf['rocketBoredomBigBoost']
            self.prestige += conf['rocketPrestigeBoost']
            self.checkBounds()
            return 0
        #fail
        self.boredom -= conf['rocketBoredomSmallBoost']
        self.prestige -= conf['rocketFail']
        if self.boredom < 0:
            self.boredom = 0
        if self.prestige < 0:
            self.prestige = 0
        self.checkBounds()
        return 1


    def holdParade(self):
        if self.cash < conf['paradeCost']:
            return 1
        self.cash -= conf['paradeCost']
        self.prestige += conf['paradeBoost'] 
        self.checkBounds()
        return 0
    
    def checkBounds(self):
        if self.happiness < 0:
            self.happiness = 0
        if self.happiness > 100:
            self.happiness = 100
        if self.hunger < 0:
            self.hunger = 0
        if self.hunger > 100:
            self.hunger = 100
        if self.boredom < 0:
            self.boredom = 0
        if self.boredom > 100:
            self.boredom = 100
        if self.prestige > 100:
            self.prestige = 100
        if self.prestige < 0:
            self.prestige = 0
        if self.cash < 0:
            self.cash = 0

    def getStatus(self):
        return  { 'id': self.name,
                'hunger': self.hunger,
                'happiness': self.happiness,
                'boredom': self.boredom,
                'prestige': self.prestige,
                'cash': self.cash,
                'events': self.events}

    

