# 📊 Economic & Industry Dashboard

## Overview
This project explores how **industry-level inventories, and new orders** interact to reveal signals about the business cycle.  

The dashboards allow users to identify:
- ⚠️ Warning signs of economic slowdown  
- 📈 Supply-demand mismatches  
- Correlations across different categories of products and even their related inventories

## Why It Matters
- **Inventories** → signal overproduction or underproduction relative to demand  
- **New Orders** → measure future demand   

Together, these indicators help businesses and analysts anticipate risks and opportunities.  

## Tech Stack
- Python (pandas, numpy)  
- Plotly Dash (interactive dashboards+ Graphing)  
- JupyterLab
- FRED API/json for economic data  
## Essentials_methods_variables.py
This is simply a local python package I made for data cleaning and graphing methods along with several other variables designed to make building dashboards from FRED more streamlined. 
## Repo Structure
project-root/
│── data-tickers/ # CSV files of data tickers which are then used to extract data from FredAPI (Inventories, New Orders, Interest)
│
│── notebooks/ # Jupyter exploration
│ ├── Inventories.ipynb
│ ├── New Orders.ipynb
│ ├── Interest Rates.ipynb
│ └── New Orders till L3.ipynb
│
│── Dashboard/ # Dash app files for deployment
│ ├── Deployment-Inventories/
│ │ └── app.py
│ ├── Deployment-New Orders/
│ │ └── app.py
│ ├── Deployment-Interest Rates/
│ │ └── app.py
│ └── combined-app/ 
│ └── app.py
│
│── requirements.txt # dependencies
│── config.json # (ignored in GitHub for security)
│── README.md # project overview
│── .gitignore # keep repo clean

## How to Run
There is no need to clone the repo since I have deployed the programs onto Render. Simply use the following links to get to the dashboard that you want. 

The first three interactive dashboards plot New Orders, Inventories, and Interest rates related to the secured overnight financing rate respectively. The final interactive dashboard allows you to see correlations across these metrics and allows you to generate your own correlation matrices with the key indicators of your choice. 

## How Inventories and New Orders Work 
This is the hierarchy for both Inventories and New Orders in terms of the subcomponents and how the graphing works (Both dashboards work the same way):

- First there is the Total Manufacturers New Orders, or Total Inventories displayed as a time series chart in the beginning, basically the aggregate overall of all the New Ordered goods or the monetary value of all inventories in the US. 

- Then, the subcomponents of that include Durable and Non-Durable goods(either New Orders or Inventory) which is shown in the first dropdown of both dashboard.  

- Finally, when you scroll down to the final dropdown, you can either see the subcomponents of the durable goods which includes the line charts for things like primary metals, electronic products, transportation equipment, etc (basically all the sectors/product types that make durable goods).

- For non-durable goods there is no known breakdown so you only see a seperate graph of that if you were to choose that option. 

(Note that the behaviour of the chart across all levels behave very differently based on if you choose to see the New Orders Dashboard or the New Inventories dashboard.)

## How does the Combined Insights Dashboard Work? 
Here, you have a dropdown with four choices:
- The first choice lets you see how Total Manufacturing New Orders and Total Inventories in the US correlate with each other
- The second choice lets you see how New Orders and Inventories for Durable and Non-Durable Goods correlate with each other
- The third choice lets you see how each sector of the Durable goods (for both inventories and new orders) correlate with each other.
- The last option allows you to pick and choose which metrics you want to see/measure correlations with from any of the three levels listed above and also the Secured Overnight Financing rate along with the SOFR volume, allowing you to pick the metrics which may be the most important for your use case.

For the custom correlation matrix, users are able to select which variables to include in the correlation matrix to explore how production behaviour evolve over time along with changes in monetary policy

## Underlying 
I truly believe that this data and this mini project done here is the first step to quantifying market demand across various goods. I think that this is a small step towards not just understanding how different business are interlaced with each other but this can also give us a feel in terms of how business cycles work. 
