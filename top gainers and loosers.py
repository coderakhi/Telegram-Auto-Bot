import pandas as pd
import requests

def get_top_loosers_nifty(urls,key,name):

        baseurl = "https://www.nseindia.com/"
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) '
                                 'Chrome/80.0.3987.149 Safari/537.36',
                   'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
        session = requests.Session()
        request = session.get(url=baseurl, headers=headers)
        cookies = dict(request.cookies)
        response1 = session.get(url=urls,headers=headers ,cookies=cookies)
        response2=response1.json()

        dicts = response2.get(key).get('data')

        lis = []
        for i in range(0, len(dicts)):
            symbol = dicts[i]['symbol']
            percentage_change = dicts[i]['perChange']
            ltp = dicts[i]['ltp']
            prev_price = dicts[i]['prev_price']

            temp = {name: symbol, 'LTP': ltp, 'pct chage': percentage_change,
                'Previous Price': prev_price}
            lis.append(temp)

        df4 = pd.DataFrame(lis)
        print(df4.head())

get_top_loosers_nifty(urls='https://www.nseindia.com/api/live-analysis-variations?index=loosers',key='NIFTY',name='Top Loosers NIFTY 50')
print(" ")
get_top_loosers_nifty(urls='https://www.nseindia.com/api/live-analysis-variations?index=loosers',key='FOSec',name='Top Loosers F&O')
print(" ")
get_top_loosers_nifty(urls='https://www.nseindia.com/api/live-analysis-variations?index=gainers',key='NIFTY',name='Top Gainers NIFTY 50')
print(" ")
get_top_loosers_nifty(urls='https://www.nseindia.com/api/live-analysis-variations?index=gainers',key='FOSec',name='Top Gainers F&O')




