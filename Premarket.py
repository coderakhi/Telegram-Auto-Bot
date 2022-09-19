import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import requests
from nsepy import get_history
from nsepy.symbols import get_symbol_list, get_index_constituents_list
import dataframe_image as dfi
import telepot


def get_pre_market_data():
    baseurl = "https://www.nseindia.com/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()



    request = session.get(baseurl, headers=headers)
    cookies = dict(request.cookies)
    url='https://www.nseindia.com/api/market-data-pre-open?key=NIFTY'

# session=requests.Session()

    request=session.get(baseurl,headers=headers,cookies=cookies)

    response=session.get(url=url,headers=headers)
    datas=response.json()

    to_scrap_value=datas['data']

    lis = []
    for item in to_scrap_value:
        symbol=item.get('metadata').get('symbol')
        pct_change=item.get('metadata').get('pChange')
        prev_price=item.get('metadata').get('previousClose')
        last_price=item.get('metadata').get('lastPrice')
        temp={'Pre Market Data Nifty(Top 5)':symbol,'Pct Change':pct_change,'Previous Close':prev_price,'Last Traded Price':last_price}
        lis.append(temp)
    df5=pd.DataFrame(lis)
    x=df5.head()
    print(x)
    lis1 = []
    for item in to_scrap_value:
        symbol=item.get('metadata').get('symbol')
        pct_change=item.get('metadata').get('pChange')
        prev_price=item.get('metadata').get('previousClose')
        last_price=item.get('metadata').get('lastPrice')
        temp={'Pre Market Data Nifty(Bottom 5)':symbol,'Pct Change':pct_change,'Previous Close':prev_price,'Last Traded Price':last_price}
        lis1.append(temp)
    df5=pd.DataFrame(lis1)
    y=df5.tail()
    print(y)

    for df in[x,y]:
        dfi.export(df, 'table.png')
        chat_id = -1001715705037
        token = '5585166082:AAESez1EURkf-Km_7xMOQ1SHCZVuLVeRyeM'

        bot = telepot.Bot(token)
        bot.sendPhoto(chat_id, photo=open('table.png', 'rb'))


get_pre_market_data()





