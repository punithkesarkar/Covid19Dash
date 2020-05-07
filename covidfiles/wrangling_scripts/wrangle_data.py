import requests
import json
import pandas as pd 
import numpy as np
from pandas.io.json import json_normalize
import datetime
import plotly.graph_objects as go
payload = {'format': 'json', 'per_page': '500', 'date':'1990:2015'}
q = requests.get('https://api.covid19api.com/dayone/country/Canada', params=payload)
canada1 = json.loads(q.text)
canada2 = json_normalize(canada1)
canada2 = canada2.replace(np.nan,0)
canada3 = canada2.groupby(['Date','Province'])[['Confirmed','Deaths',"Recovered",'Active']].mean()
canada3 = canada3.reset_index()
canada3 = canada3[canada3['Province']!='']
canada3['Date'] = pd.to_datetime(canada3['Date'])
canada4 = canada3.copy()
canada4['day'] = canada4['Date'].dt.day_name()
canada4 = canada4[canada4['Date']=='2020-05-04']
# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart

canada5 =  canada2[canada2['Province']=='']
conf = canada5['Confirmed'].values
conf2 = canada5['Active'].values
conf3 = canada5['Deaths'].values

fig = go.Figure()

fig.add_trace(go.Indicator(
    value = conf[0],
    delta = {'reference': 160},
    gauge = {'axis': {'visible': False}},
    title = {'text': "Confirmed"},
    domain = {'row': 0, 'column': 0}))


fig.add_trace(go.Indicator(
    mode = "number",
    value = conf2[0],
    title = {'text': "Active"},
    domain = {'row': 0, 'column': 1}))

fig.add_trace(go.Indicator(
    mode = "delta",
    value = -conf3[0],
    title = {'text': "Deaths"},
    domain = {'row': 0, 'column': 2}))

fig.update_layout(
    grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
       
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 90}}]
                         }})
# third chart plots percent of population that is rural from 1990 to 2015
    
  

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=canada4['Province'],
        y=canada4['Deaths'],
        name="Deaths"
    ))

fig.add_trace(
    go.Bar(
        x=canada4['Province'],
        y=canada4['Confirmed'],
        name="Confirmed"
    ))
fig.update_layout(title_text='Confirmed vs Death Cases ' + str(datetime.datetime.today().date()), title_x=0.5)
fig.update_xaxes(title_text='Province')
fig.update_yaxes(title_text='Cases')
fig.show()

# second chart plots ararble land for 2015 as a bar chart    
import plotly.graph_objects as go

canada3['Date'] = pd.to_datetime(canada3['Date'])
fig = go.Figure(data=[
    go.Bar(name='Confirmed', x=canada3['Date'], y=canada3['Confirmed']),
    go.Bar(name='Deaths', x=canada3['Date'], y=canada3['Deaths']),
    go.Bar(name='Active', x=canada3['Date'], y=canada3['Active'])
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(title_text='Confirmed, Active and Death Cases Per Day', title_x=0.5)
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Cases')
fig.show()


    
