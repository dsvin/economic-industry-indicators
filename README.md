# 📊 Economic & Industry Dashboard

## Overview
This project explores how **industry-level inventories, new orders, and interest rates** interact to reveal signals about the business cycle.  

The dashboards allow users to identify:
- ⚠️ Warning signs of economic slowdown  
- 📈 Supply-demand mismatches  
- 💰 Effects of monetary policy on industry performance  

## Why It Matters
- **Inventories** → signal overproduction or underproduction relative to demand  
- **New Orders** → measure future demand  
- **Interest Rates** → drive financing costs and demand cycles  

Together, these indicators help businesses and analysts anticipate risks and opportunities.  

## Tech Stack
- Python (pandas, numpy)  
- Plotly Dash (interactive dashboards+ Graphing)  
- JupyterLab
- FRED API/json for economic data  

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
│ └── combined-app/ # (future) regression/combined analysis
│ └── app.py
│
│── requirements.txt # dependencies
│── config.json # (ignored in GitHub for security)
│── README.md # project overview
│── .gitignore # keep repo clean

## How to Run
There is no need to clone the repo since I have deployed the programs onto Render. Simply use the following links to get to the dashboard that you want. 

Note that the first three are simply just dashboards with graphs used for the purpose of gathering data. 
**The finished product is the last dashboard that combines everything to deliver key insights.**  