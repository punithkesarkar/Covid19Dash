import requests
import json
import pandas as pd 
import numpy as np
from pandas.io.json import json_normalize
import datetime
import plotly.graph_objects  as go
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
    canada5 =  canada2[canada2['Province']=='']
    canada5['Date'] =  pd.to_datetime(canada5['Date'] )
    canada5 = canada5[canada5['Date']=='2020-05-04']
    conf = canada5['Confirmed'].values
    conf2 = canada5['Active'].values
    conf3 = canada5['Deaths'].values
    graph_one = []

    import plotly.graph_objects as go
    graph_one = go.Figure()
    graph_one.add_trace(
            go.Indicator(
            value = conf[0],
            delta = {'reference': 160},
            gauge = {'axis': {'visible': False}},
            title = {'text': "Confirmed"},
            domain = {'row': 0, 'column': 0}))


    graph_one.add_trace(
            go.Indicator(
            mode = "number",
            value = conf2[0],
            title = {'text': "Active"},
            domain = {'row': 1, 'column': 0}))
    
    graph_one.add_trace(go.Indicator(
            mode = "delta",
            value = -conf3[0],
            title = {'text': "Deaths"},
            domain = {'row': 2, 'column': 0}))

    graph_one.update_layout(
            title=("Overview"),
            grid = {'rows': 3, 'columns': 3, 'pattern': "independent"},
            template = {'data' : {'indicator': [{

                'mode' : "number+delta+gauge",
                'delta' : {'reference': 90}}]
                                 }})
    
    layout_one = dict(title = 'Current State of Coronavirus in Canada'
                )
    

    layout_one = dict(
                xaxis = dict(title = 'Date',),
                yaxis = dict(title = 'Cases'),
                )
                
    graph_two = []
    
    graph_two.append(
          go.Bar(name='Deaths', x=canada3['Date'], y=canada3['Deaths'])
      )

    layout_two = dict(title = 'Number of Deaths per Day',
                xaxis = dict(title = 'Date',),
                yaxis = dict(title = 'Cases'),
                )
    
    graph_three = []

    
    
    

    from plotly import tools    
    trace1 = go.Bar(name='Confirmed', x=canada3['Date'], y=canada3['Confirmed'])
    trace2 = go.Bar(name='Active', x=canada3['Date'], y=canada3['Active'])  
    graph_three = tools.make_subplots(rows=1, cols=1,  shared_xaxes=True)

    graph_three.append_trace(trace2, 1,1)
    graph_three.append_trace(trace1, 1, 1)
    graph_three.update_yaxes(title_text="Cases", row=1, col=1)
    graph_three.update_xaxes(title_text="Date", row=1, col=1)
    graph_three['layout'].update(title='Number of Confirmed vs Active Cases per Day')
    layout_three = dict(
                xaxis = dict(title = 'Date', ),
                yaxis = dict(title = 'Cases'),
                )

    
    graph_four=[]
    import plotly.graph_objects as go
    graph_four = go.Figure()

    graph_four.add_trace(
        go.Scatter(
            x=canada4['Province'],
            y=canada4['Deaths'],
            name="Deaths"
        ))

    graph_four.add_trace(
        go.Bar(
            x=canada4['Province'],
            y=canada4['Confirmed'],
            name="Confirmed"
        ))
    graph_four.update_layout(title_text='Confirmed vs Death Cases per Province') 
    graph_four.update_xaxes(title_text='Province')
    graph_four.update_yaxes(title_text='Cases')
    
    layout_four = dict(
                xaxis = dict(title = 'Province', ),
                yaxis = dict(title = 'Cases'),
                )
    
    graph_five=[]
    canada6 = canada4[['Province','Confirmed','Deaths','Active']]
    graph_five = go.Figure(data=[go.Table(
    header=dict(values=list(canada6.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[canada6.Province, canada6.Confirmed, canada6.Deaths, canada6.Active],
               fill_color='lavender',
               align='left'))])
    graph_five.update_layout(title_text='Confirmed, Deaths and Active Cases Per Province') 
    layout_five = dict(
                xaxis = dict(title = 'Province', ),
                yaxis = dict(title = 'Cases'),
                )    
    graph_six=[]
    canada6 = canada3[['Date','Confirmed','Deaths','Active']]
    canada6['Date'] = pd.to_datetime(canada6['Date'])
    canada6['Date'] = canada6["Date"].dt.date
    canada7 = canada6.groupby('Date').agg({'Confirmed':'sum','Deaths':'sum','Active':'sum'}).reset_index()
    canada7 = canada7.sort_values(by=['Date'],ascending=False)
    graph_six = go.Figure(data=[go.Table(
    header=dict(values=list(canada7.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[canada7.Date, canada7.Confirmed, canada7.Deaths, canada7.Active],
               fill_color='lavender',
               align='left'))])
    graph_six.update_layout(title_text='Confirmed, Deaths and Active Cases Per Day') 
    layout_six = dict(
                xaxis = dict(title = 'Province', ),
                yaxis = dict(title = 'Cases'),
                )                   
      # append all charts
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_six, layout=layout_six))
    figures.append(dict(data=graph_five, layout=layout_five))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    
    

    return figures    

return_figures()
