#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from fredapi import Fred
import plotly.graph_objects as go
import dash
from dash import html, dcc, Input, Output, callback
import json

with open("config.json") as f:
    config = json.load(f)


# In[2]:


#Introducting the api-key and style changes
plt.style.use('fivethirtyeight')
fkey = config["api_key"]

#Dataframe configurations
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)


# In[3]:


# Creating FRED object:
fred = Fred(api_key=fkey)

#Simplified series datapoints for graphing
def series(series_id):
    return fred.get_series(series_id)


# In[4]:


#Creating a function that does data cleaning on the Series provided given the code
def data_cleaning(code):
    #Get the data from the FRED API
    data  = fred.get_series(code)
    #Convert the data to a pandas DataFrame
    data = pd.DataFrame(data)
    #Convert the index to a datetime object
    data.index = pd.to_datetime(data.index)
    #Convert the index to a column
    data['Date'] = data.index
    # Change the column name to Value
    data.rename(columns={0: 'Value'}, inplace=True)
    #Reorder the columns to have Date first
    data = data[['Date', 'Value']]
    #Convert the date column to a datetime object
    data['Date'] = pd.to_datetime(data['Date'])
    #reset the index
    data.reset_index(drop=True, inplace=True)
    # Drop the rows with missing values in the values column
    data.dropna(subset=['Value'], inplace=True)
    return data


# In[5]:


#Reading our csv file
df = pd.read_csv('Interest.csv')

#Building functions to convert a table into graphs :))
def grapher(var):
    API = var['FRED API CODE'].tolist()
    Measure = var['Measure'].tolist()
    data1 = []
    for i in range(0,len(API)):
        clean = data_cleaning(API[i])
        data1.append(go.Scatter(x = clean['Date'],y=clean['Value'],name=Measure[i]))
    graph = go.Figure(data = data1)
    graph = graph.update_layout(xaxis_rangeslider_visible=True)
    return graph
    
def grapher1(var1):
    API = var1['FRED API CODE']
    Measure = var1['Measure']
    clean = data_cleaning(API)
    data11 = go.Scatter(x= clean['Date'],y=clean['Value'],name=Measure)
    graph1 = go.Figure(data = data11)
    graph1 = graph1.update_layout(xaxis_rangeslider_visible=True)
    return graph1


# In[6]:


#Creating our graphs :)

#SOFR
sofr = df.iloc[0]
gsofr = grapher1(sofr)

#SOFR percentiles
sofrl1 = df.iloc[1:5]
gsofrl1 = grapher(sofrl1)

#SOFR Volume stuff
sofrv = df.iloc[5]
gsofrv = grapher1(sofrv)


# In[10]:


#Creating our Dash Application!
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Dashboard for SOFR Interest Rates'),

    html.Div(children=
        '''Secured Overnight Financing Rate (Left) and Volume (Right) Graphs'''
    ),
    html.Div([
    dcc.Graph(id='SOFR',figure=gsofr, style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(id='SOFRV',figure=gsofrv,style={'width': '48%', 'display': 'inline-block'})])
    ,
    dcc.Dropdown(id='tmSub', options = [
        {'label':'Show Percentiles', 'value':'TMS'}
    ], placeholder="Toggle :)"
                ),
    html.Div(id ='TMSS'), html.Div(id='dropdown2'), html.Div(id='Level-2')
    
])

#Call back function for the first component:
@app.callback(
    Output('TMSS', 'children'),
    Input('tmSub', 'value')
)
def update_graph(select):
    if select == 'TMS':
        return dcc.Graph(figure=gsofrl1)
    else:
        return html.Div()

#Run Web application
if __name__ == '__main__':
    app.run(debug=True,port = 8053)


# In[ ]:
