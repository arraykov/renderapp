import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_ag_grid as dag

# Load your DataFrame from the CSV file
df = pd.read_csv('Watchlist.csv')

df['Current Yield'] = df['Current Yield'].astype(str).str.replace('%', '')
df['Current Yield'] = pd.to_numeric(df['Current Yield'], errors='coerce')

columns_to_convert = ["3m Z", "6m Z", "1y Z", "PriceΔ", "NAV%Δ", "NAVΔ", "Premium/Discount", "Current Yield"]

for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')

dollar_columns = ["Price", "NAV"]
for column in dollar_columns:
    df[column] = df[column].apply(lambda x: f'${x:.2f}' if pd.notnull(x) else x)


styleConditionsForZScores = {
    "styleConditions": [
        {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
        {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
    ]
}

filterParams = {
    "buttons": ['apply', 'reset'],
    "closeOnApply": True,
}

columnDefs = [
    
        
        
            {"field": "Ticker", "cellRenderer": "StockLink", "filter": "agTextColumnFilter", "filterParams": filterParams, "floatingFilter": True},
            {"field": "Nav Ticker", "filter": "agTextColumnFilter", "filterParams": filterParams},
            {"field": "Premium/Discount", "filter": "agNumberColumnFilter", "filterParams": filterParams},
        
    
    {
        "headerName": "Z-Scores",
        "children": [
            {"field": "3m Z", "cellStyle": styleConditionsForZScores, "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "6m Z", "cellStyle": styleConditionsForZScores, "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "1y Z", "cellStyle": styleConditionsForZScores, "filter": "agNumberColumnFilter", "filterParams": filterParams},
        ]
    },
    {"field": "Price", "filter": "agNumberColumnFilter", "filterParams": filterParams},
    {"field": "PriceΔ", "cellStyle": styleConditionsForZScores, "filter": "agNumberColumnFilter", "filterParams": filterParams},
    {
        "headerName": "NAV",
        "children": [
            {"field": "NAV", "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "NAV%Δ", "cellStyle": styleConditionsForZScores, "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "NAVΔ", "cellStyle": styleConditionsForZScores, "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "52W NAV Avg", "columnGroupShow": "open", "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "52W NAV Low", "columnGroupShow": "open", "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "52W NAV High", "columnGroupShow": "open", "filter": "agNumberColumnFilter", "filterParams": filterParams},
        ]
    },
    {
        "headerName": "Fundamentals",
        "children": [
            {"field": "Category", "suppressSizeToFit": True, "width": 250, "filter": "agTextColumnFilter", "filterParams": filterParams, "floatingFilter": True},
            {"field": "Current Yield", "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "Distribution Amount", "filter": "agNumberColumnFilter", "filterParams": filterParams},
            {"field": "Distribution Frequency", "columnGroupShow": "open", "filter": "agTextColumnFilter", "filterParams": filterParams},
            {"field": "Fiscal Year End", "columnGroupShow": "open", "filter": "agTextColumnFilter", "filterParams": filterParams},
        ]
    },
]

defaultColDef = {
    "resizable": True,
    "initialWidth": 200,
    "wrapHeaderText": True,
    "autoHeaderHeight": True,
    "sortable": True,
    "filter": "agMultiColumnFilter",
    "filterParams": filterParams,
    "enableRowGroup": False,
    "enableValue": False,
    "enablePivot": False,
}

def generate_dashboard():
    table = dag.AgGrid(
        id='table',
        columnDefs=columnDefs,
        rowData=df.to_dict('records'),
        style={"height": "1250px", "width": "100%"},
        columnSize="responsiveSizeToFit",
        defaultColDef=defaultColDef,
        dashGridOptions={
            "autopaginationAutofPageSize": True,
            "animateRows": True, 
        },
    )
    return table

external_stylesheets = ['/custom.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    generate_dashboard()
])

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')