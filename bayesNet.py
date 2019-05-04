# Arthor: Andrew Lewis
# Project 3: CPSC 352
# April 24th 2019

import random

# conditional probability tables for the Bayesian network as
# a dictionary.  
# 
# The key is a string tuple describing the node.
# Entries are stored as ordered dictionary pairs

bn = {'Course':[[],{'long':0.5, 'short':0.5}],
      'Weather':[[],{'coldWet':0.3, 'hot':0.2, 'nice':0.5}],
      'HarePerf':[['Course','Weather'],
               {('short','coldWet'):{'slow':0.5,'medium':0.3,'fast':0.2},
               ('short','hot'):{'slow':0.1,'medium':0.2,'fast':0.7},
                ('short','nice'):{'slow':0.0,'medium':0.2,'fast':0.8},
                ('long','coldWet'):{'slow':0.7,'medium':0.2,'fast':0.1},
                ('long','hot'):{'slow':0.2,'medium':0.4,'fast':0.4},
                ('long','nice'):{'slow':0.1,'medium':0.3,'fast':0.6}}],
      'TortoisePerf':[['Course', 'Weather'],
                {('short','coldWet'):{'slow':0.2,'medium':0.3,'fast':0.5},
                ('short','hot'):{'slow':0.4,'medium':0.5,'fast':0.1},
                ('short','nice'):{'slow':0.3,'medium':0.5,'fast':0.2},
                ('long','coldWet'):{'slow':0.2,'medium':0.4,'fast':0.4},
                ('long','hot'):{'slow':0.2,'medium':0.5,'fast':0.3},
                ('long','nice'):{'slow':0.4,'medium':0.4,'fast':0.2}}],
      'HareWins':[['HarePerf', 'TortoisePerf'],
                   {('slow','slow'):{'win':0.5},('slow','medium'):{'win':0.1},('slow','fast'):{'win':0.0},
                   ('medium','slow'):{'win':0.8},('medium','medium'):{'win':0.5},('medium','fast'):{'win':0.2},
                   ('fast','slow'):{'win':0.9},('fast','medium'):{'win':0.7},('fast','fast'):{'win':0.5}}]}

# a list of the variables, starting "from the bottom" of the network.
# in topological ordering towards the top
varss = ['Weather','Course','HarePerf','TortoisePerf','HareWins']

# compute probability that var has the value val.  e are the list of
# variable values we already know, and bn has the conditional probability
# tables.
def Pr(var, e, bn):
    parents = bn[var][0]
    parentVals = ()
    # debugprint('Pr***', var, e, bn, parents)
    if len(parents) == 0:
        table = bn[var][1]
        # print(table)
    else:
        # debugprint('   Pr***')
        for parent in parents:
            # print('Var ', e[parent], parent)
            parentVals+=(e[parent])
        table = bn[var][1][parentVals]
        # print(table)
    return table
    
# Generate 
def generateSample(algo, bn, varss, weather = None, course = None):
    # list of generated samples
    e = {}
    if weather is not None:
        e['Weather'] = (weather,)

    if course is not None:
        e['Course'] = (course,)

    for var in varss:
        # pick a value for var according to the probabilities in bn and the
        # ones we already picked.
        if var == 'Weather' and weather is not None:
            continue
        if var == 'Course' and course is not None:
            continue

        r = random.uniform(0.0,1.0)
        probabilities = Pr(var,e,bn)
        lastProb = 0.0
        # print(r)
        for x in probabilities:
            if r <= lastProb+probabilities[x] and r > lastProb:
                e[var] = (x,)
                # print('chosen ', e[var])
                break
            else:
                lastProb+=probabilities[x]
        if 'HareWins' not in e:
            e['HareWins'] = ('lose',)
        
    # return the sample - e
    if algo == 'prior':
        if e['HareWins'] == ('win',):
            return 1
        return 0
    if algo == 'reject':
        return e

# Generates samples and return probability of HareWins
def priorSample(n, weather = None, course = None):
    wins = 0.0
    total = n
    for i in range(n):
        wins+=generateSample('prior',bn, varss, weather, course)    
    if wins is not 0:
        return wins/n
    else:
        return 'No wins'

# Loop through generated samples and filters accordingly
def rejectionSample(n, weather = None, course = None, HarePerf = None, TortoisePerf = None, HareWins = None):
    finalSamples = []
    for i in range(0, n):
        sample = generateSample('reject', bn,varss)
        #print(sample)
        if weather is not None and sample['Weather'] != (weather,):
            # print(weather)
            continue
        if course is not None and sample['Course'] != (course,):
            # print(sample['Course'])
            continue
        if HarePerf is not None and sample['HarePerf'] != (HarePerf,):
            continue
        if TortoisePerf is not None and sample['TortoisePerf'] != (TortoisePerf,):
            continue
        if HareWins is not None and sample['HareWins'] != (HareWins,):
            #print(sample)
            continue
        finalSamples.append(sample) 
        #print(finalSamples)  
    return finalSamples    
   

while True:
    x = input('''"Enter number corresponding to the queries below
    1. In general, how likely is the Hare to win?
    2. Given that is it coldWet, how likely is the Hare to win?
    3. Given that the Tortoise won on the short course, what is the probability distribution for the Weather?"''')
    print("")
    if x == '1' or x == 1: 
        print(priorSample(10000))
        continue
    if x == '2' or x == 2:
        print(priorSample(10000, 'coldWet'))
    if x == '3' or x == 3:
        coldWet = 0.0
        hot = 0.0
        nice = 0.0

        for s in rejectionSample(10000, course = 'short', HareWins='lose'):
            if s['Weather'] == ('coldWet',):
                coldWet+=1.0
            if s['Weather'] == ('hot',):
                hot+=1.0
            if s['Weather'] == ('nice',):
                nice+=1.0

        total = coldWet + hot + nice
        print(total)
        print('coldWet: ', coldWet/total)
        print('Hot: ', hot/total)
        print('Nice: ', nice/total)
