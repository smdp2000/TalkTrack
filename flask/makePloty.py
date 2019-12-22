#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from ipywidgets import Output, VBox
import os


# In[2]:


def check_file (file):

    try:
        with open(file) as f:
            f.close ()

    except IOError:
        open (file, 'x')
        with open (file, 'w') as f:
            json.dump ({}, f)


# In[3]:


def sentiments (data):
    
    check_file ('database.json')
   
    for id in data:
        max = data [id]['neutral']
        sentiment = 'neutral'
        if max < data [id]['negative']:
            max = data [id]['negative']
            sentiment = 'negative'
        elif max < data [id]['positive']:
            max = data [id]['positive']
            sentiment = 'positive'
    
        sent_dict = {id: {
                        'sentiment': sentiment,
                        'value': max}
                    }
        
        with open ('database.json') as f:
            database = json.load (f)
            database.update (sent_dict)
        with open ('database.json', 'w') as f:
            json.dump (database, f)


# In[4]:


def plot_sentiment (data):
    
    sentiments (data)
    
    count_negative = 0
    count_positive = 0
    count_neutral = 0
    
    positiv = []
    negative = []
    neutral = []
   
    with open ('database.json') as f:
        database = json.load (f)
    
    check_file ('sentiment_data.json')
    for id in database:
        
        if database [id]['sentiment'] == 'neutral':
            count_neutral += 1
            neutral.append (id)
        elif database [id]['sentiment'] == 'negative':
            count_negative += 1
            negative.append (id)
        elif database [id]['sentiment'] == 'positive':
            count_positive += 1
            positiv.append (id)
    
    s_data = {'positive': positiv, 'negative': negative, 'neutral': neutral}
    with open ('sentiment_data.json') as s:
        sent_data = json.load (s)
        
    sent_data.update (s_data)
    with open ('sentiment_data.json', 'w') as s:
        json.dump (sent_data, s)
    
    count = [count_neutral, count_positive, count_negative]
    lable = ['Neutral', 'Positive', 'Negative']
    colours = ['b', 'g', 'r']
    
    fig = go.Figure(data=[go.Pie(labels=lable, values=count,pull=[0.025,0.025,0.025], name="Sentiment",
                                title = 'Sentiment',
                                text=[sent_data ['neutral'], sent_data ['positive'], sent_data ['negative']],
                                hovertemplate = "%{label}: %{text}",
                                marker=dict(colors=colours,
                                line=dict(color='#000000', width=2)))])
    
    fig.write_image ("/home/ankit/Desktop/project/flask/sentiment.png")


# In[5]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[6]:


def taxonomy (data):
    
    check_file ('database.json')
   
    for id in data:
        max = 0.0
        for i in data [id]:
            if max < i ['confidence_score']:
                max = i ['confidence_score']
                tag = i ['tag']
        
        with open ('database.json') as f:
            database = json.load (f)
            database [id]['tag'] = tag;
            database [id]['confidence_score'] = max
        with open ('database.json', 'w') as f:
            json.dump (database, f)


# In[7]:


def plot_taxonomy (data):
    
    taxonomy (data)
    
    check_file ('taxonomy_data.json')
   
    with open ('database.json') as f:
        database = json.load (f)
    with open ('taxonomy_data.json') as f:
        tax = json.load (f)
        
    for id in database:
        
        tag = database [id]['tag']
        flag = 1
        if tag in tax:
            for i in tax [tag]:
                for key in i:
                    if id in key: 
                        flag = 0
                        break
            if flag:
                tax [tag].append ({id: database [id]['confidence_score']})
        else:
            tax [tag] = [{id: database [id]['confidence_score']}]

    with open ('taxonomy_data.json', 'w') as f:
        json.dump (tax, f)
        
    with open ('taxonomy_data.json') as f:
        tax = json.load (f)
        
    count = []
    label_tax = []
    text = []
    for tag in tax:
        count.append (len (tax [tag]))
        label_tax.append (tag)
        t = []
        for i in tax [tag]:
            for val in i:
                t.append (val)
        text.append (t)
        
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', '#fe100f', '#92f09d']
    
    col = []
    exp = []
    for l in range (len (label_tax)):
        col.append (colours [l])
        exp.append (0.025)
    
    fig = go.Figure(data=[go.Pie(labels=label_tax, values=count,pull=exp, name="Taxonomy",
                                title = 'Taxonomy',
                                text=text,
                                hovertemplate = "%{label}: %{text}",
                                marker=dict(colors=col,
                                line=dict(color='#000000', width=2)))])
    
    fig.write_image ("/home/ankit/Desktop/project/flask/taxonomy.png")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[8]:


def abuse (data):
    
    check_file ('database.json')
    
    for id in data:
        max = data [id]['abusive']
        lang = 'abusive'
        if max < data [id]['hate_speech']:
            max = data [id]['hate_speech']
            lang = 'hate_speech'
        elif max < data [id]['neither']:
            max = data [id]['neither']
            lang = 'neither'
        
        with open ('database.json') as f:
            database = json.load (f)
            database [id]['language'] = lang
            database [id]['abuse'] = max
        with open ('database.json', 'w') as f:
            json.dump (database, f)


# In[9]:


def plot_abuse (data):
    
    abuse (data)
    
    check_file ('abuse_data.json')
    
    count_abusive = 0
    count_hatespeech = 0
    count_neither = 0
    
    abusive = []
    hatespeech = []
    neither = []
   
    with open ('database.json') as f:
        database = json.load (f)
        
    for id in database:
        
        if database [id]['language'] == 'abusive':
            count_abusive += 1
            abusive.append (id)
        elif database [id]['language'] == 'hate_speech':
            count_hatespeech += 1
            hatespeech.append (id)
        elif database [id]['language'] == 'neither':
            count_neither += 1
            neither.append (id)
    
    lang_data = {'abusive': abusive, 'hate_speech': hatespeech, 'neither': neither}
    with open ('abuse_data.json') as s:
        abuse_data = json.load (s)
        
    abuse_data.update (lang_data)
    with open ('abuse_data.json', 'w') as s:
        json.dump (abuse_data, s)
    
    count = [count_abusive, count_hatespeech, count_neither]
    lable = ['Abusive', 'Hate Speech', 'Neither']
    colours = ['k', 'r', 'g']
    
    fig = go.Figure(data=[go.Pie(labels=lable, values=count,pull= [0.025,0.025,0.025], name="Abuse",
                                title = 'Abuse',
                                text=[abuse_data ["abusive"], abuse_data ["hate_speech"], abuse_data ["neither"]],
                                hovertemplate = "%{label}: %{text}",
                                marker=dict(colors=colours,
                                line=dict(color='#000000', width=2)))])
    
    fig.write_image ("/home/ankit/Desktop/project/flask/abuse.png")


# In[ ]:





# In[ ]:





# In[ ]:





# In[10]:


def intent (data):
    
    check_file ('database.json')
    
    for id in data:
        max = 0.0
        for i in data [id]:
            if max < data [id][i]:
                max = data [id][i]
                intent = i
        
        with open ('database.json') as f:
            database = json.load (f)
            database [id]['intent'] = intent;
            database [id]['intent_val'] = max
        with open ('database.json', 'w') as f:
            json.dump (database, f)


# In[11]:


def plot_intent (data):
    
    intent (data)
    
    check_file ('intent_data.json')
    
    with open ('intent_data.json', 'w') as f:
        json.dump ({}, f)
    
    with open ('database.json') as f:
        database = json.load (f)
    with open ('intent_data.json') as f:
        intnt = json.load (f)
        
    for id in database:
        
        intention = database [id]['intent']
        flag = 1
        if intention in intnt:
            for i in intnt [intention]:
                for key in i:
                    if id in key: 
                        flag = 0
                        break
            if flag:
                intnt [intention].append ({id: database [id]['intent_val']})
        else:
            intnt [intention] = [{id: database [id]['intent_val']}]

    with open ('intent_data.json', 'w') as f:
        json.dump (intnt, f)
        
    with open ('intent_data.json') as f:
        intnt = json.load (f)
        
    count = []
    label_intent = []
    text = []
    for intention in intnt:
        count.append (len (intnt [intention]))
        label_intent.append (intention)
        t = []
        for i in intnt [intention]:
            for val in i:
                t.append (val)
        text.append (t)
        
    colours = ['b', 'g', 'r', 'c', 'm']
    
    col = []
    exp = []
    for l in range (len (label_intent)):
        col.append (colours [l])
        exp.append (0.05)
    
    fig = go.Figure(data=[go.Pie(labels=label_intent, values=count,pull= exp, name="Intent",
                                title = 'Intention',
                                text=text,
                                hovertemplate = "%{label}: %{text}",
                                marker=dict(colors=colours,
                                line=dict(color='#000000', width=2)))])
    
    fig.write_image ("/home/ankit/Desktop/project/flask/intent.png")


# In[ ]:





# In[ ]:





# In[ ]:




