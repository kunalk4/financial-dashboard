import pandas as pd
import plotly
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from alpha_vantage.timeseries import TimeSeries

key = 'YB1PO7823Q6SQVYL'
ts = TimeSeries(key, output_format='pandas')

#-------------------------------------------------------------------------------
# Building our Web app and update financial data automatically

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Kunal's Stock Performance App", style={"fontSize": 24}),
    dcc.Interval(
                id='my_interval',
                n_intervals=0,       # number of times the interval was activated
                interval=24*3600*1000,   # update every day (24 hours)
    ),
    dcc.Graph(id="world_finance"),   # empty graph to be populated by line chart
])

#-------------------------------------------------------------------------------
@app.callback(
    Output(component_id='world_finance', component_property='figure'),
    [Input(component_id='my_interval', component_property='n_intervals')]
)
def update_graph(n):
    """Pull financial data from Alpha Vantage and update graph every 24 hours"""

    ttm_data, ttm_meta_data = ts.get_intraday(symbol='TTM', interval="60min", outputsize='compact')
    ttm_data.to_csv("pre_processed_data", encoding='utf-8')
    df = ttm_data.copy()
    df=df.transpose()
    df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
                     "4. close":"close","5. volume":"volume"},inplace=True)
    df=df.reset_index().rename(columns={'index': 'indicator'})
    df = pd.melt(df,id_vars=['indicator'],var_name='Date',value_name='Stock Price')
    df = df[df['indicator']!='volume']
    print(df[:15])
    df.to_csv('trade_data.csv', encoding='utf-8')

    line_chart = px.line(
                    data_frame=df,
                    x='Date',
                    y='Stock Price',
                    color='indicator',
                    title="Stock: {}".format(ttm_meta_data['2. Symbol'])
                 )
    return (line_chart)

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)