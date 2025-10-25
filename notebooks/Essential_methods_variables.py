import pandas as pd
import plotly.express as px
import requests
from fredapi import Fred
import plotly.graph_objects as go
import dash
from dash import html, dcc, Input, Output, callback
import json

#Variables Section
with open("../config.json") as f:
    config = json.load(f)

fkey = config["api_key"]
fred = Fred(api_key=fkey)


df_interest = pd.read_csv('../data-tickers/Interest.csv')
df_inventories = pd.read_csv('../data-tickers/Inventories.csv')
df_orders = pd.read_csv('../data-tickers/newOrders.csv')




#Methods Section


#Simplified series datapoints for graphing
def series(series_id,fred=fred):
    return fred.get_series(series_id)

#Creating a function that does data cleaning on the Series provided given the code
def data_cleaning(code):
    #Get the data from the FRED API
    data  = series(code)
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

#Building functions to convert a table into graphs :))
def grapher(var):
    API = var['FRED API Code'].tolist()
    Measure = var['Measure'].tolist()
    data1 = []
    for i in range(0,len(API)):
        clean = data_cleaning(API[i])
        data1.append(go.Scatter(x = clean['Date'],y=clean['Value'],name=Measure[i]))
    graph = go.Figure(data = data1)
    graph = graph.update_layout(xaxis_rangeslider_visible=True, xaxis_title='Date', yaxis_title='Value',title=Measure[i])
    return graph

def grapher1(var1):
    API = var1['FRED API Code']
    Measure = var1['Measure']
    clean = data_cleaning(API)
    data11 = go.Scatter(x= clean['Date'],y=clean['Value'],name=Measure)
    graph1 = go.Figure(data = data11)
    graph1 = graph1.update_layout(xaxis_rangeslider_visible=True, xaxis_title='Date', yaxis_title='Value',title=Measure)
    return graph1
