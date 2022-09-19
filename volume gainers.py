import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import requests
from nsepy import get_history
from nsepy.symbols import get_symbol_list, get_index_constituents_list


baseurl = "https://www.nseindia.com/"
url = "https://www.nseindia.com/api/live-analysis-most-active-securities?index=volume"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}

session = requests.Session()
request = session.get(baseurl, headers=headers)
cookies = dict(request.cookies)




response = session.get(url, headers=headers, cookies=cookies)
datas=response.json()



result=[]

for lst in datas['data']:
     company=lst['symbol']
     symbol=lst['identifier']
     purpose=lst['purpose']
     temp={'symbol':symbol,'compnay':company,}
     result.append(temp)

df=pd.DataFrame(result)

list1=list(df['compnay'])

nifty_stocks=get_index_constituents_list('NIFTY')
list2=list(nifty_stocks['Symbol'])

result2=[]
for item in  list1:
    for items in list2:
        if item==items:
            temp={'Volume Gainers Index Stocks':item}
            result2.append(temp)

df2=pd.DataFrame(result2)
print(df2.head())
