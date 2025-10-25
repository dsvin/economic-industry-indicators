#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import requests
from fredapi import Fred
import plotly.graph_objects as go
import dash
from dash import html, dcc, Input, Output, callback
import json
import Essential_methods_variables as emv
import plotly.express as px
import importlib
import numpy as np

importlib.reload(emv)



# In[17]:


emv.df_interest
df_I = emv.df_interest[(emv.df_interest["FRED API CODE"]=="SOFR")|(emv.df_interest["FRED API CODE"]=="SOFRVOL")]
df_I = df_I.rename(columns={"FRED API CODE":"FRED API Code"})
df_I


# In[14]:


df_total_OI = pd.concat([emv.df_orders[emv.df_orders['Level']==0],emv.df_inventories[emv.df_inventories['Level']==0]])
df_one_OI = pd.concat([emv.df_orders[emv.df_orders['Level']==1],emv.df_inventories[emv.df_inventories['Level']==1]])

df_two_OI = pd.concat([emv.df_orders[emv.df_orders['Level']==2],emv.df_inventories[emv.df_inventories['Level']==2]])

def update_measure(row):
    code = str(row["FRED API Code"])
    measure = row["Measure"]
    if code.endswith("I"):
        return "Inv: " + measure
    else:
        return measure

df_total_OI["Measure"] = df_total_OI.apply(update_measure,axis =1)
df_one_OI["Measure"] =  df_one_OI.apply(update_measure,axis =1)
df_two_OI["Measure"] =  df_two_OI.apply(update_measure,axis =1)
df_combined = pd.concat([df_total_OI,df_one_OI,df_two_OI,df_I])

def data_clean_matrix(bracket,matrix=True):
    check = []
    x = pd.DataFrame()
    for i,j in zip(bracket["FRED API Code"],bracket["Measure"]):
        y = emv.data_cleaning(i)
        y.rename(columns={'Value':j},inplace=True)
        check.append(y.shape[0])
        if x.empty:
            x = y 
        else:
            x = x.merge(y, on = 'Date')
    #print(f"{max(check)-min(check)} monthly datapoint(s) are being lost in the process")
    if matrix:
        corr_df = x[bracket["Measure"]]
        corr_matrix = corr_df.corr(method = 'pearson')
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        corr_mask = corr_matrix.mask(mask)
        
        fig  = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title='Correlation Heatmap:',
            zmin = -1, zmax=1
        )
        fig.update_layout(height=900,width=900)
        return fig
        
    return x





level_0 = data_clean_matrix(df_total_OI)
level_1 = data_clean_matrix(df_one_OI)
level_2 = data_clean_matrix(df_two_OI)

def custom_choice(l):
    x=[]
    for i in list(l["Measure"]):
        #x.append(i)
        x.append({"label":i,"value":i})
    return x



        
    


# In[14]:


#Insight: The demand for computer and electronic product is not correlated with any other demand or inventory amount,
#It is almost as its own thing, which is really interesting. Except for inventory of comp and electric products. (For level 2)

#Insight: For level 1, it seems like Durable, Nondurable and its correponding inventories move almost in unison with each other,
#with a high correlation

#Level 0 is the same as level 1. 


# In[18]:


app  = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children="Movement Correlations of Inventories and New Orders"),
    dcc.Dropdown(id='pearson',options = [
        {"label":"Aggregate Inventories and Orders","value":"agg"},
        {"label":"Durable and Non-Durable Goods","value":"dnd"},
        {"label":"Durable Goods subcomponents","value":"durable"},
        {"label":"Create your Own","value":"custom"}
    ],placeholder="select which correlations you would like to see"),
    html.Div(id="graph"),
])

@app.callback(
    Output('graph','children'),
    Input('pearson','value')
)
def update_graph(select):
    if select == "agg":
        return html.Div([dcc.Graph(figure=level_0),html.Div("📈🔗📉For both the aggregate measures and also the Durable vs Non-Durable it appears that both new orders and inventories move in unison with each other. However, when selecting durable good subcomponents, it can be noticed that the demand for new orders of computer and electronic products is not correlated with any other category of durable goods regardless of whether that is new orders or inventory. This can be a potential insight for business diversification", 
             style={"backgroundColor": "#e7f5ff", "padding": "8px", "borderRadius": "8px", "marginBottom": "6px"})])
    elif select == "dnd":
        return html.Div([dcc.Graph(figure=level_1),html.Div("📈🔗📉For both the aggregate measures and also the Durable vs Non-Durable it appears that both new orders and inventories move in unison with each other. However, when selecting durable good subcomponents, it can be noticed that the demand for new orders of computer and electronic products is not correlated with any other category of durable goods regardless of whether that is new orders or inventory. This can be a potential insight for business diversification", 
             style={"backgroundColor": "#e7f5ff", "padding": "8px", "borderRadius": "8px", "marginBottom": "6px"})])
    elif select == "durable":
        return html.Div([dcc.Graph(figure=level_2),html.Div("📈🔗📉For both the aggregate measures and also the Durable vs Non-Durable it appears that both new orders and inventories move in unison with each other. However, when selecting durable good subcomponents, it can be noticed that the demand for new orders of computer and electronic products is not correlated with any other category of durable goods regardless of whether that is new orders or inventory. This can be a potential insight for business diversification", 
             style={"backgroundColor": "#e7f5ff", "padding": "8px", "borderRadius": "8px", "marginBottom": "6px"})])
    elif select == "custom":
        return html.Div([
            dcc.Dropdown(value=[],placeholder="Aggregate Measures",id="agg1",options=custom_choice(df_total_OI),multi=True),
            dcc.Dropdown(value=[],placeholder="Durable and Non-Durable Aggregates",id="dnd1",options=custom_choice(df_one_OI),multi=True),
            dcc.Dropdown(value=[],placeholder="Durable Goods",id='durable1',options=custom_choice(df_two_OI),multi=True),
            dcc.Dropdown(id="sofr_interest",value=[],placeholder="Secured Overnight Financing Rate metrics",options=custom_choice(df_I),multi=True),
        html.Div(id="graph_one")]),
            
    else:
        return html.Div()

@app.callback(
    Output('graph_one','children'),
    Input('agg1','value'),
    Input('dnd1','value'),
    Input('durable1','value'),
    Input('sofr_interest','value')
)

def custom_matrix(zero,one,two,interest):
    global df_combined
    three = zero+one+two+interest
    dfcm = pd.DataFrame()
    if three != [] and len(three)>=2:
        for i in zero+one+two+interest:
            dfcm = pd.concat([dfcm,df_combined[df_combined["Measure"]==i]])
        return dcc.Graph(figure =data_clean_matrix(dfcm))
    else:
        return "You must select at least two values across any of the three dropdowns to check correlations"


