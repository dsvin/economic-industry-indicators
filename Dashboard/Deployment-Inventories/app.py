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


plt.style.use('fivethirtyeight')

fkey = config["api_key"]

#Creating a keyword search function
def fred_search(search_text, api_key=fkey, limit=100):
    url = f"https://api.stlouisfed.org/fred/series/search?search_text={search_text}&api_key={api_key}&file_type=json&limit={limit}"
    response = requests.get(url)
    return pd.DataFrame(response.json()['seriess'])

#Get category id based on series id
def category(series_id, api_key=fkey):
    url = f"https://api.stlouisfed.org/fred/series/categories?series_id={series_id}&api_key={api_key}&file_type=json"
    response = requests.get(url).json()
    return response 

#Get the subcategories of the categories and their names along with category ids
def children(cid, api_key=fkey):
    url = f"https://api.stlouisfed.org/fred/category/children?category_id={cid}&api_key={api_key}&file_type=json"
    response = requests.get(url).json()
    return response

#Get series datapoints for graphing
def values(series_id,api_key = fkey):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
    response = requests.get(url).json()
    return pd.DataFrame(response['observations'])
#Make pandas dataframe to show all the columns on one line
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


#Reading CSV file: 
df = pd.read_csv('Inventories.csv')
#Level 0 
TM = data_cleaning('AMTMTI') #Total Manufacturing 

#Level 1
Durable = data_cleaning('AMDMTI') #Durable Goods

nonDurable = data_cleaning('AMNMTI')

#Level 2 Under Durable
durablesL2 = df[df['Level']==2]
durablesL2[['FRED API Code','Measure']]
twoAPI = durablesL2['FRED API Code'].tolist()
twoMeasure = durablesL2['Measure'].tolist()
twoData = []
for i in range(0,len(twoAPI)):
    xy = data_cleaning(twoAPI[i])
    twoData.append(go.Scatter(x=xy['Date'],y=xy['Value'],name=twoMeasure[i]))


# In[6]:


#Total manufacturing graph
trace1 = go.Scatter(x=TM['Date'],y=TM['Value'],name='Total Manufacturing')
figTM = go.Figure(data=[trace1])
figTM = figTM.update_layout(xaxis_rangeslider_visible=True, xaxis_title='Date', yaxis_title='Value', title="Total Inventories")

#Durable and Non-durable Goods (Level 1)

graphDurableNon = go.Scatter(x=nonDurable['Date'],y=nonDurable['Value'],name='Non-Durable Goods')
graphDurable = go.Scatter(x=Durable['Date'],y=Durable['Value'],name = 'Durable Goods')
figDND = go.Figure(data=[graphDurableNon, graphDurable])
figDND = figDND.update_layout(xaxis_rangeslider_visible=True, xaxis_title='Date', yaxis_title='Value', title="Durable and Non-Durable")


#Durable Goods all Subcomponents Graph: 
twoGraph = go.Figure(data=twoData)
twoGraph = twoGraph.update_layout(xaxis_rangeslider_visible=True, xaxis_title='Date', yaxis_title='Value', title="Durable Inventories Subcomponents")

#


# In[13]:


# starting the Dash application: 
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dashboard for Inventories'),

    html.Div(children=
        '''Total Manufacturing'''
    ),

    dcc.Graph(
        id='totalManufacturing',
        figure=figTM
    ),
    dcc.Dropdown(id='tmSub', options = [
        {'label':'Show Subcomponents', 'value':'TMS'}
    ], placeholder="Toggle :)"
                ),
    html.Div(id ='TMSS'), html.Div(id='dropdown2'), html.Div(id='Level-2')
    
])

#Call back function for the first component:
@callback(
    Output('TMSS', 'children'), Output('dropdown2','children'),
    Input('tmSub', 'value')
)
def update_graph(select):
    if select == 'TMS':
        return (html.Div([dcc.Graph(figure=figDND),html.Div("📈 Despite overlap/occasional converging of durable and non-durable goods when it comes to the amount of orders, There is no overlap here showing that the durable inventory in terms of value is generally higher than non-durable goods", 
             style={"backgroundColor": "#e7f5ff", "padding": "8px", "borderRadius": "8px", "marginBottom": "6px"})]),
                dcc.Dropdown(id='dropdown_2', options = [
                    {'label':'Non-Durable Goods','value':'NDG'},
                    {'label':'Durable Goods','value':'DG'}
                ],placeholder="Show next subcomponents")
               )
    else:
        return html.Div(), html.Div()
#Callback function for the level 2 subcomponents
@callback(
    Output('Level-2','children'), Input('dropdown_2','value'), allow_duplicate = True
)

def update_graph2(choose):
    if choose =='NDG':
        chosen = go.Figure(data=[graphDurableNon])
        chosen = chosen.update_layout(xaxis_rangeslider_visible=True, xaxis_title='Date', yaxis_title='Value', title="Non-Durable Inventories")
        return dcc.Graph(figure=chosen)
    elif choose == 'DG':
        return dcc.Graph(figure= twoGraph), html.Div([
    html.Div("📈 We can see that transportation equipment has increased uniformly, to accomodate for the recent sudden increases in New Orders.  ", 
             style={"backgroundColor": "#E97451", "padding": "8px", "borderRadius": "8px", "marginBottom": "6px"})
])
    else:
        return html.Div()

#Run Web application
if __name__ == '__main__':
    app.run(debug=True,port = 8051)



# In[11]:


get_ipython().system('python -m jupyter nbconvert --to script "Inventories.ipynb"')

