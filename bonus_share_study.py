import yfinance as yf
import datetime
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.graph_objs as go

pd.options.plotting.backend = "plotly"


ticker_list = [
    'CDSL.NS', 'BPCL.NS', 'GAIL.NS', 'DABUR.NS', 'IOC.NS',
    'RELIANCE.NS', 'ITC.NS', 'INFY.NS', 'WIPRO.NS', 'TCS.NS', 'ONGC.NS']
announce_dates = [
    '2024-08-13', '2024-06-13', '2022-08-23', '2010-09-03', '2022-06-13',
    '2017-08-31', '2016-05-24', '2018-08-27', '2019-02-25', '2018-05-21',
    '2016-12-06']

returns_pre = []
returns_post = []
returns_nifty_pre = []
returns_nifty_post = []
ex_dates = []
action_dfs = []
for i in range(len(ticker_list)):
    # i=0
    ticker = ticker_list[i]
    print(ticker)
    scrip = yf.Ticker(ticker)

    # Get dividend and stock split dates
    actions_df = scrip.actions
    # print(actions_df)
    actions_df['Date'] = actions_df.index
    non_zero_dates = actions_df[actions_df['Stock Splits'] != 0]['Date']
    action_dfs.append(non_zero_dates)
    dt_object = non_zero_dates.iloc[-1]

    # Format as "YYYY-MM-DD"
    ex_date = dt_object.strftime("%Y-%m-%d")
    ex_dates.append(ex_date)
    post_ex_date = (dt_object + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    # pre_ex_date = (dt_object - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    pre_ex_date = announce_dates[i]
    stock_data = yf.Ticker(ticker)
    pre_ex_data = stock_data.history(start=pre_ex_date, end=ex_date)
    nifty_data_pre = yf.download('^NSEI', start=pre_ex_date, end=ex_date, actions=True)
    nifty_data_post = yf.download('^NSEI', start=ex_date, end=post_ex_date, actions=True)
    returns_nifty1 = 100*((nifty_data_pre.iloc[-1]['Close'] - nifty_data_pre.iloc[0]['Close'])/nifty_data_pre.iloc[0]['Close'])
    returns_nifty2 = 100*((nifty_data_post.iloc[-1]['Close'] - nifty_data_post.iloc[0]['Close'])/nifty_data_post.iloc[0]['Close'])
    returns_nifty_pre.append(returns_nifty1)
    returns_nifty_post.append(returns_nifty2)
    returns1 = 100*((pre_ex_data.iloc[-1]['Close'] - pre_ex_data.iloc[0]['Close'])/pre_ex_data.iloc[0]['Close'])
    print(f'returns: {round(returns1,2)}%')
    returns_pre.append(returns1)
    post_ex_data = stock_data.history(start=ex_date, end=post_ex_date)
    returns2 = 100*((post_ex_data.iloc[-1]['Close'] - post_ex_data.iloc[0]['Close'])/post_ex_data.iloc[0]['Close'])
    returns_post.append(returns2)
    print(f'returns: {round(returns2,2)}%')

df_returns = pd.DataFrame({'ticker':ticker_list,'announce_date':announce_dates,'ex_date':ex_dates,
                           'returns_pre':returns_pre,'returns_nifty_pre':returns_nifty_pre,
                           'returns_post':returns_post,'returns_nifty_post':returns_nifty_post})

df_returns.to_csv(r'C:\Users\alex1\df_returns.csv', header= True)

fig = go.Figure()

fig.add_trace(go.Bar(x=df_returns['ticker'], y=df_returns['returns_pre'], name='Returns Pre'))
fig.add_trace(go.Bar(x=df_returns['ticker'], y=df_returns['returns_post'], name='Returns Post'))

fig.update_layout(
    title='Stock Returns Pre vs. Post Announcement',
    xaxis_title='ticker',
    yaxis_title='Returns (%)',
    barmode='group'
)

# Show the chart
plot(fig)
