# this is going to call the CPI, FED Rate, S&P 500, and ETH
# we want to return the previous 6 months of data for each of these, in a dict of lists


from dbObject import dbObject
import requests
import datetime
import os

class EconObject:
    def __init__(self):
        self.alphav_api_key = os.getenv('ALPHAV_API_KEY')
        self.today = datetime.date.today()

    def get_cpi_data(self , num_months=6):
        url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={self.alphav_api_key}'
        r = requests.get(url)
        data = r.json() 

        timeframe_data = data['data'][:num_months] # get last num_months of data
        # returns a list of dicts [{'date': '2023-10-01', 'value': '307.671'}, {'date': '2023-09-01', 'value': '307.789'}, {'date': '2023-08-01', 'value': '307.026'}, {'date': '2023-07-01', 'value': '305.691'}, {'date': '2023-06-01', 'value': '305.109'}]

        return timeframe_data
    
    def get_fed_data(self , num_months=6):
        url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={self.alphav_api_key}'
        r = requests.get(url)
        data = r.json() 

        timeframe_data = data['data'][:num_months] # get last num_months of data
        # returns a list of dicts 

        return timeframe_data

    def get_stock_data(self, symbol, num_days=10):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=compact&symbol={symbol}&apikey={self.alphav_api_key}' # change output size if you want deep historical data, changed symbol for differnt one
        r = requests.get(url)
        data = r.json()

        daily_data = data.get('Time Series (Daily)', {}) # extract the data part of the json
        sorted_dates = sorted(daily_data.keys(), reverse=True) # sort in desc
        recent_dates = sorted_dates[:num_days] # gets the last num_days of dates, this accounts for days when the market is closed. its just a list of dates

        close_prices = [{'date':date, 'close_price':daily_data[date]['4. close']} for date in recent_dates] # makes a list of dicts with those dates

        return close_prices
    
    def get_crypto_data(self, symbol, num_days=14):
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={self.alphav_api_key}'
        r = requests.get(url)
        data = r.json()

        daily_data = data.get('Time Series (Digital Currency Daily)', {}) # extract the data part of the json
        sorted_dates = sorted(daily_data.keys(), reverse=True) # sort in desc
        recent_dates = sorted_dates[:num_days]

        close_prices = [{'date':date, 'close_price':daily_data[date]['4b. close (USD)']} for date in recent_dates]

        return close_prices
    
    def get_gdp_data(self, num_quarters=6):
        url = f'https://www.alphavantage.co/query?function=REAL_GDP&interval=quarterly&apikey={self.alphav_api_key}'
        r = requests.get(url)
        data = r.json()
        timeframe_data = data['data'][:num_quarters] # get last num_quarters of data

        return timeframe_data
    
    def get_unemployment_data(self, num_months=12):
        url = f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={self.alphav_api_key}'
        r = requests.get(url)
        data = r.json()
        timeframe_data = data['data'][:num_months] # get last num_months of data

        return timeframe_data
    
    def get_oil_data(self, num_months=6):
        url = f'https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey={self.alphav_api_key}'
        r = requests.get(url)
        data = r.json()
        timeframe_data = data['data'][:num_months] # get last num_months of data

        return timeframe_data

    def get_fear_greed(self):
        url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
        headers = {
            "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
            "X-RapidAPI-Host": "fear-and-greed-index.p.rapidapi.com"
        }

        r = requests.get(url, headers=headers)
        data = r.json()
        # {'now': {'value': 67, 'valueText': 'Greed'}, 'previousClose': {'value': 66, 'valueText': 'Greed'}, 'oneWeekAgo': {'value': 66, 'valueText': 'Greed'}, 'oneMonthAgo': {'value': 32, 'valueText': 'Fear'}, 'oneYearAgo': {'value': 75, 'valueText': 'Extreme Greed'}}

        return data['fgi']


    def get_econ_data(self):
        # markets
        fear_greed_data = self.get_fear_greed()
        sp500_data = self.get_stock_data('SPY', 10) # symbol, timeframe. num of days to get, default 10, don't forget there are none on weekends
        housing_data = self.get_stock_data('ITB', 130) # this is a housing and construction etf
        eth_data = self.get_crypto_data('ETH', 14) # num of days to get, default 14

        # economy
        gdp_data = self.get_gdp_data(4) # pass num of quarters in desired timeframe, def 6
        cpi_data = self.get_cpi_data(6) # you can pass in a number of months to get, default 6
        fed_data = self.get_fed_data(6) # pass in num of months, default 6
        unemp_data = self.get_unemployment_data(12) # pass in num of months, default 12
        crude_oil_data = self.get_oil_data(6) # pass in num of months, default 6

        print('Economic Data Updated')

        econ_data = {
            'markets':{
                'fear_greed':fear_greed_data, 
                'sp500':sp500_data, 
                'itb':housing_data, 
                'eth':eth_data
                }, 
            'economy':{
                'gdp':gdp_data, 
                'cpi':cpi_data, 
                'fed':fed_data, 
                'unemployment':unemp_data, 
                'oil':crude_oil_data
                }
            }

        return econ_data


'''
EXAMPLE RETURN ECON DATA

{
'markets':{
        'fear_greed':[
            {'now': {'value': 67, 'valueText': 'Greed'}, 'previousClose': {'value': 66, 'valueText': 'Greed'}, 'oneWeekAgo': {'value': 66, 'valueText': 'Greed'}, 'oneMonthAgo': {'value': 32, 'valueText': 'Fear'}, 'oneYearAgo': {'value': 75, 'valueText': 'Extreme Greed'}}
        ], 
        'sp500':[
            {'date': '2021-11-01', 'close_price': '459.92'}, 
            {'date': '2021-10-29', 'close_price': '459.92'}, 
            {'date': '2021-10-28', 'close_price': '459.92'}, 
            {'date': '2021-10-27', 'close_price': '459.92'}, 
            {'date': '2021-10-26', 'close_price': '459.92'}, 
            {'date': '2021-10-25', 'close_price': '459.92'}, 
            {'date': '2021-10-22', 'close_price': '459.92'}, 
            {'date': '2021-10-21', 'close_price': '459.92'}, 
            {'date': '2021-10-20', 'close_price': '459.92'}, 
            {'date': '2021-10-19', 'close_price': '459.92'}
        ], 
        'itb':[
            {'date': '2021-11-01', 'close_price': '459.92'}, 
            {'date': '2021-10-29', 'close_price': '459.92'}, 
            {'date': '2021-10-28', 'close_price': '459.92'}, 
            {'date': '2021-10-27', 'close_price': '459.92'}, 
            {'date': '2021-10-26', 'close_price': '459.92'}, 
            {'date': '2021-10-25', 'close_price': '459.92'}, 
            {'date': '2021-10-22', 'close_price': '459.92'}
        ],
        'eth':[
            {'date': '2021-11-01', 'close_price': '459.92'}, 
            {'date': '2021-10-29', 'close_price': '459.92'}, 
            {'date': '2021-10-28', 'close_price': '459.92'}, 
            {'date': '2021-10-27', 'close_price': '459.92'}, 
            {'date': '2021-10-26', 'close_price': '459.92'}, 
            {'date': '2021-10-25', 'close_price': '459.92'}, 
            {'date': '2021-10-22', 'close_price': '459.92'}
        ]
    },

'economy':{
        'gdp':[
            {'date': '2023-10-01', 'value': '307.671'}, 
            {'date': '2023-09-01', 'value': '307.789'}, 
            {'date': '2023-08-01', 'value': '307.026'}, 
            {'date': '2023-07-01', 'value': '305.691'}, 
            {'date': '2023-06-01', 'value': '305.109'}
        ],
        'cpi':[
            {'date': '2023-10-01', 'value': '307.671'}, 
            {'date': '2023-09-01', 'value': '307.789'}, 
            {'date': '2023-08-01', 'value': '307.026'}, 
            {'date': '2023-07-01', 'value': '305.691'}, 
            {'date': '2023-06-01', 'value': '305.109'}
        ],
        'fed':[
            {'date': '2023-11-01', 'value': '5.33'}, 
            {'date': '2023-10-01', 'value': '5.33'}, 
            {'date': '2023-09-01', 'value': '5.33'}, 
            {'date': '2023-08-01', 'value': '5.33'}, 
            {'date': '2023-07-01', 'value': '5.12'}, 
            {'date': '2023-06-01', 'value': '5.08'}
        ],
        'unemployment':[
            {'date': '2023-11-01', 'value': '5.33'}, 
            {'date': '2023-10-01', 'value': '5.33'}, 
            {'date': '2023-09-01', 'value': '5.33'}, 
            {'date': '2023-08-01', 'value': '5.33'}, 
            {'date': '2023-07-01', 'value': '5.12'}, 
            {'date': '2023-06-01', 'value': '5.08'}
        ],
        'oil':[
            {'date': '2023-11-01', 'value': '5.33'}, 
            {'date': '2023-10-01', 'value': '5.33'}, 
            {'date': '2023-09-01', 'value': '5.33'}, 
            {'date': '2023-08-01', 'value': '5.33'}, 
            {'date': '2023-07-01', 'value': '5.12'}, 
            {'date': '2023-06-01', 'value': '5.08'}
        ]
    }
}
'''

# econ_obj = EconObject()
# # db_obj = dbObject()

# econ_obj.get_gdp_data()