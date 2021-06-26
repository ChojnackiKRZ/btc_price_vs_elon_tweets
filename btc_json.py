# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:33:59 2021

@author: krzys
"""
"""
To make sure twint works:
pip install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
"""
import twint
import nest_asyncio
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt 


nest_asyncio.apply()

"""user and topics of interests"""
c = twint.Config()
c.Username = 'elonmusk'
keys = ['bitcoin', 'btc']

"""path with working folder and tweets storage in tweets.json file"""
path = r'C:\Users\krzys\Desktop\data science\II semestr\Big Data\projekt\data_json\tweets.json'
os.chdir(r'C:\Users\krzys\Desktop\data science\II semestr\Big Data\projekt')

"""delete current file if existing not to append tweets to file but to create
new one"""
try:
    os.remove(path)
except:
    pass

"""scrapping tweets according to parameters"""
for i in keys:
    c.Search = i
    c.Store_json = True
    c.Output = 'data_json'
    a = twint.run.Search(c)

"""json to pandas"""
data = pd.read_json(path, lines = True)

"""btc parameters: dates from and to. I want to test BTC price changes with
    elon musks' tweets so I take from date as the first tweet about BTC"""
date_to = str(max (data['date']))[:10]
date_from = str(min (data['date']))[:10]
address = 'https://api.coindesk.com/v1/bpi/historical/close.json?start={}&end={}'.format(date_from, date_to)
price_btc = requests.get(address).json()

"""tweets numbers"""
count_by_date = data.groupby(['date']).count()['id']

"""btc price"""
price_btc = price_btc['bpi']

"""pandas frame conversion and naming columns"""
price_btc_pandas = pd.DataFrame(data=price_btc.items())
price_btc_pandas.columns = ['date', 'price']

"""datetime conversion and index setup"""
price_btc_pandas['date'] = pd.to_datetime(price_btc_pandas['date'])
price_btc_pandas = price_btc_pandas.set_index('date')

"""two frames concat and nan fill-up"""
resampling_btc = price_btc_pandas['price'].resample('M').mean()
resampling_tweets = count_by_date.resample('M').max().fillna(0)
result = pd.concat([resampling_btc, resampling_tweets], axis = 1)

"""plots with secondary axis"""
result['id'].plot(lw = '2', color = 'red', figsize=(10,5))
    #renaming x axis
plt.xlabel('date')
    #renaming y axis
plt.ylabel('number of tweets')
    #plot on secondary y axis
ax = result['price'].plot(secondary_y = True, lw = 2, colormap = 'jet', \
                          marker = '.', markersize = '10', \
                          title = "btc price $ vs Elon Musk's tweets")
    #naming secondary y axis
ax.set_ylabel("btc price in $")

    #saving chart
fig = ax.get_figure()
fig.savefig("chart.png")


"""correlation and p value test"""
print (40*"xx")
from scipy.stats import ttest_ind
p_value = ttest_ind(resampling_btc, resampling_tweets).pvalue

if p_value < 0.05:
    corr = resampling_btc.corr(resampling_tweets)
    if corr > 0:
        if abs (corr) < 0.2:
            print ("No linear connection between Elon Musk's tweets and BTC price")
        elif abs (corr) > 0.2 and corr < 0.4:
            print ("Weak linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go up) as number of tweets changes (goes up).\
                       IT IS NOT CAUSTAION.")
        elif abs (corr) > 0.4 and corr < 0.7: 
            print ("Moderate linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go up) as number of tweets changes (goes up).\
                       IT IS NOT CAUSTAION.")
        elif abs (corr) > 0.7 and corr < 0.9: 
            print ("Strong linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go up) as number of tweets changes (goes up).\
                       IT IS NOT CAUSTAION.")
        elif abs (corr) > 0.9: 
            print ("Very strong linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go up) as number of tweets changes (goes up).\
                       IT IS NOT CAUSTAION.")
    elif corr < 0:
        if abs (corr) < 0.2:
            print ("No linear connection between Elon Musk's tweets and BTC price")
        elif abs (corr) > 0.2 and corr < 0.4:
            print ("Weak linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go down) as number of tweets changes (goes down).\
                       IT IS NOT CAUSTAION.")
        elif abs (corr) > 0.4 and corr < 0.7: 
            print ("Moderate linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go down) as number of tweets changes (goes down).\
                       IT IS NOT CAUSTAION.")
        elif abs (corr) > 0.7 and corr < 0.9: 
            print ("Strong linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go down) as number of tweets changes (goes down).\
                       IT IS NOT CAUSTAION.")
        elif abs (corr) > 0.9: 
            print ("Very strong linear connection between Elon Musk's tweets and BTC price.\
                   BTC seems to change (go down) as number of tweets changes (goes down).\
                       IT IS NOT CAUSTAION.")
    else:
        print ("Correlation = 0. No linear connection.")
else:
    print ("BTC price does not correlate with Elon Musk's tweets")
    

