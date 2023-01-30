import pandas as pd
import plotly
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# "pip install alpha_vantage" (if you haven't done so)
from alpha_vantage.timeseries import TimeSeries

#-------------------------------------------------------------------------------
# Set up initial key and financial category
key = 'YB1PO7823Q6SQVYL' 

# Chose your output format or default to JSON (python dict)
ts = TimeSeries(key, output_format='pandas') # 'pandas' or 'json' or 'csv'

# Get the data, returns a tuple
# ttm_data is a pandas dataframe, ttm_meta_data is a dict
ttm_data, ttm_meta_data = ts.get_intraday(symbol='TTM', interval="60min", outputsize='compact')
print(ttm_meta_data)

df = ttm_data.copy()
print(df.head(15))
print(df.columns)

df=df.transpose()
print(df.head())

df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
                 "4. close":"close","5. volume":"volume"},inplace=True)
df=df.reset_index().rename(columns={'index': 'indicator'})
print(df.head())

df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
df = df[df['indicator']!='volume']
print(df[:15])