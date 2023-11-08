import dash
from dash import dcc, html, dash_table, Dash
from dash.dependencies import Input, Output
from dash.dash_table.Format import Format  # Import the Format class from dash_table
import pandas as pd
import dash_ag_grid as dag


# Load your DataFrame from the CSV file
df = pd.read_csv('Watchlist.csv')

# Convert the "Premium/Discount" column to string, remove the percentage sign, and convert to numeric
df['Current Yield'] = df['Current Yield'].astype(str).str.replace('%', '')
df['Current Yield'] = pd.to_numeric(df['Current Yield'], errors='coerce')

# List of columns to convert to numeric
columns_to_convert = ["3m Z", "6m Z", "1y Z", "PriceΔ", "NAV%Δ", "NAVΔ","Premium/Discount"]  # Add more columns as needed

# Convert the specified columns to numeric
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')
# Format specific columns as dollars
dollar_columns = ["Price", "NAV"]  # Add more columns as needed
for column in dollar_columns:
    df[column] = df[column].apply(lambda x: f'${x:.2f}' if pd.notnull(x) else x)


columnDefs = [

    {
        "headerName": "",
        "children": 
        [{"field": "Ticker", "sortable": True,"cellRenderer":"StockLink"},
        {"field": "Nav Ticker", "sortable": True},
        {"field": "Premium/Discount", "sortable": True},  
        ]    
    },
    {
        "headerName": "Z-Scores",
        "children": [
            {"field": "3m Z", "filter": "agNumberColumnFilter", "sortable": True, "cellStyle": {
                "styleConditions": [
                    {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                    {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
                ]
            }},
            {"field": "6m Z", "filter": "agNumberColumnFilter", "sortable": True, "cellStyle": {
                "styleConditions": [
                    {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                    {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
                ]
            }},
            {"field": "1y Z", "filter": "agNumberColumnFilter", "sortable": True, "cellStyle": {
                "styleConditions": [
                    {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                    {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
                ]
            }},
        ]
    },
    {"field": "Price", "sortable": True},
    {"field": "PriceΔ", "sortable": True, "cellStyle": {
            "styleConditions": [
                {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
            ]
        }},
    # NAV group
    {
        "headerName": "NAV",
        "children": [
            {"field": "NAV", "sortable": True},
            {"field": "NAV%Δ", "sortable": True, "cellStyle": {
                "styleConditions": [
                    {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                    {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
                ]
            }},
            {"field": "NAVΔ", "sortable": True, "cellStyle": {
                "styleConditions": [
                    {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                    {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
                ]
            }},
            {"field": "52W NAV Avg", "sortable": True, "columnGroupShow": "open"},
            {"field": "52W NAV Low", "sortable": True, "columnGroupShow": "open"},
            {"field": "52W NAV High", "sortable": True, "columnGroupShow": "open"},
        ]
    },

    {
        "headerName": "Fundamentals",
        "children": [{"field": "Category" , "sortable": True, "suppressSizeToFit":True, "width":250 },
        {"field": "Current Yield", "sortable": True},
        {"field": "Distribution Amount", "sortable": True},
        {"field": "Distribution Frequency", "sortable": True, "columnGroupShow": "open"},
        {"field": "Fiscal Year End", "sortable": True, "columnGroupShow": "open"},
        ]
    },
]

defaultColDef = {
    "resizable": True,
    "initialWidth": 200,
    "wrapHeaderText": True,
    "autoHeaderHeight": True,
    "sortable": True,
    "filter": True,
    "enableRowGroup": False,
    "enableValue": False,
    "enablePivot": False,
}

sidebarDef = {
    "toolPanels": [
        {
            "id": "columns",
            "labelDefault": "Columns",
            "labelKey": "columns",
            "iconKey": "columns",
            "toolPanel": "agColumnsToolPanel",
            "toolPanelParams": {
                    "suppressColumnFilter": True,
                    "suppressColumnSelectAll": True,
                    "suppressColumnExpandAll": False,
                    "suppressPivotMode": True,
                    "suppressRowGroups": True,
                    "suppressValues": True,
                    
        }},
        {
            "id": "filters",
            "labelDefault": "Filters",
            "labelKey": "filters",
            "iconKey": "filter",
            "toolPanel": "agFiltersToolPanel",
            "toolPanelParams": {
                "suppressFilterSearch": True,
            }
        },
        # Add other panels as needed
    ],
    "defaultToolPanel": None  # This will open the columns tool panel by default when the sidebar is shown
}


# Create the AGGrid component
table = dag.AgGrid(
    id='table',
    columnDefs=columnDefs,
    rowData=df.to_dict('records'),
    style={"height": "1250px", "width": "100%"},
    columnSize="responsiveSizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={
                    "autopaginationAutofPageSize": True,
                    "sideBar": sidebarDef,
                    "animateRows": True, 
                    "skipHeaderOnAutoSize": True,                                          
    },
    enableEnterpriseModules= True,
)

external_stylesheets = [
    'custom.css'  # your custom stylesheet
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    [table],
    style={"margin": 20},)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
