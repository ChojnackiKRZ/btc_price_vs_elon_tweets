# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:33:59 2021

@author: krzys
"""
"""
Aby twint działał poprawnie, należy pobrać wg poniższego:
pip install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
Niestety nie dostałem jeszcze dostępu do API twittera, to muszę sobie te dane
zescrapować, stad twint
"""
import twint
import nest_asyncio
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt 


nest_asyncio.apply()

"""deklaruję użytkownika oraz tematy, które mnie interesują"""
c = twint.Config()
c.Username = 'elonmusk'
keys = ['bitcoin', 'btc']

"""sciezka z dostępem do tweetow (path) oraz zmiana folderu roboczego"""
path = r'C:\Users\krzys\Desktop\data science\II semestr\Big Data\projekt\data_json\tweets.json'
os.chdir(r'C:\Users\krzys\Desktop\data science\II semestr\Big Data\projekt')

"""usuwam obecny plik aby nie dokładać do niego kolejnych tweetow tylko 
ładować obecne"""
try:
    os.remove(path)
except:
    pass

"""szukanie tweetow po zadanch parametrach, zwraca plik w formacie json"""
for i in keys:
    c.Search = i
    c.Store_json = True
    c.Output = 'data_json'
    a = twint.run.Search(c)

"""przerabianie pliku z tweetami na ramkę w pandas"""
data = pd.read_json(path, lines = True)

"""btc: od kiedy do kiedy dane oraz pobieranie danych o cenie w $"""
date_to = str(max (data['date']))[:10]
date_from = str(min (data['date']))[:10]
address = 'https://api.coindesk.com/v1/bpi/historical/close.json?start={}&end={}'.format(date_from, date_to)
price_btc = requests.get(address).json()

"""licznik tweetow"""
count_by_date = data.groupby(['date']).count()['id']

"""cena btc"""
price_btc = price_btc['bpi']

"""konwersja na ramkę pandas, zmiana nazwy kolumn"""
price_btc_pandas = pd.DataFrame(data=price_btc.items())
price_btc_pandas.columns = ['date', 'price']

"""konwersja na datetime, zmiana indeksu ramki"""
price_btc_pandas['date'] = pd.to_datetime(price_btc_pandas['date'])
price_btc_pandas = price_btc_pandas.set_index('date')

"""łączenie ramki ilosci tweetow i ceny btc oraz wypełnienie wartosci nan"""
resampling_btc = price_btc_pandas['price'].resample('M').mean()
resampling_tweets = count_by_date.resample('M').max().fillna(0)
result = pd.concat([resampling_btc, resampling_tweets], axis = 1)

"""rysowanie wykresow z osią pomocniczą dla ilosci tweetów oraz zmiana nazw"""
result['id'].plot(lw = '2', color = 'red', figsize=(10,5))
    #zmiana nazwy dla glownej osi x
plt.xlabel('date')
    #zmiana nazwy dla glownej osi y
plt.ylabel('number of tweets')
    #rysowanie wykresu na osi pomocniczej
ax = result['price'].plot(secondary_y = True, lw = 2, colormap = 'jet', \
                          marker = '.', markersize = '10', \
                          title = "btc price $ vs Elon Musk's tweets")
    #zmiana nazwy dla osi pomocniczej y
ax.set_ylabel("btc price in $")

    #zapis wykresu do folderu roboczego
fig = ax.get_figure()
fig.savefig("chart.png")
