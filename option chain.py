import requests
import pandas as pd
from ratelimit import limits
from backoff import on_exception, expo
from ratelimit.exception import RateLimitException
import datetime as dt
import dataframe_image as dfi
import telepot


@on_exception(expo,RateLimitException, max_tries=15)
@limits(calls=1, period=1)
def get_option_chain(symbol, expiry_date):

    url = f'https://www.nseindia.com/api/option-chain-indices?symbol={symbol}'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    if response.status_code!=200:
        raise RateLimitException("OPPS!! NSE Blocked me", 30)

    dict = response.json()

    dict1 = dict['records']['data']

    result = []
    result1 = []
    for item in dict1:
        CE = item.get('CE')
        PE = item.get('PE')

        if CE is not None:
            result.append(CE)
        if PE is not None:
            result1.append(PE)

    df = pd.DataFrame(result)
    df1 = pd.DataFrame(result1)


    mapping = {
        'strikePrice': 'Strike Price',
        'expiryDate': 'Expiry Date',
        'underlying': 'Underlying',
        'openInterest': 'Open Interest',
        'changeinOpenInterest': 'Change in OI',
        'pchangeinOpenInterest': 'Pct Change in OI',
        'totalTradedVolume': 'Traded Volume',
        'impliedVolatility': 'IV',
        'lastPrice': 'Last Price'

    }

    df0 = df.rename(columns=mapping)
    result = df0[mapping.values()]
    df1 = df1.rename(columns=mapping)
    result1 = df1[mapping.values()]

    condition = result['Expiry Date'] == expiry_date
    condition1 = result1['Expiry Date'] == expiry_date

    result=result[condition]
    result1=result1[condition1]

    Max_call_OI = result['Open Interest'].max()
    Max_Put_OI = result1['Open Interest'].max()


    x='Max Call OI Strike for',expiry_date, symbol, result.loc[result['Open Interest'] == Max_call_OI, 'Strike Price'
    y='Max Put OI Strike for',expiry_date, symbol, result1.loc[result1['Open Interest'] == Max_Put_OI, 'Strike Price'

    # for i in [Max_call_OI,Max_Put_OI]:
    dfi.export(, 'tables.png')
    chat_id = -1001715705037
    token = '5585166082:AAESez1EURkf-Km_7xMOQ1SHCZVuLVeRyeM'

    bot = telepot.Bot(token)
    bot.sendPhoto(chat_id, photo=open('tables.png', 'rb'))



get_option_chain(symbol='NIFTY', expiry_date='14-Jul-2022')
print(" ")
get_option_chain(symbol='BANKNIFTY', expiry_date='14-Jul-2022')

