import dash
from dash import dcc, html, dash_table, Dash
from dash.dependencies import Input, Output
from dash.dash_table.Format import Format  # Import the Format class from dash_table
import pandas as pd
import dash_ag_grid as dag


# Load your DataFrame from the CSV file
df = pd.read_csv('src/Watchlist.csv')

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
    {"field": "Ticker", "sortable": True,"cellRenderer":"StockLink"},
    {"field": "Nav Ticker", "sortable": True},
    {"field": "Category" , "sortable": True, "suppressSizeToFit":True, "width":250 },
    {"field": "3m Z", "sortable": True, "cellStyle": {
            "styleConditions": [
                {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
            ]
        }},
    {"field": "6m Z", "sortable": True, "cellStyle": {
            "styleConditions": [
                {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
            ]
        }},
    {"field": "1y Z", "sortable": True, "cellStyle": {
            "styleConditions": [
                {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
            ]
        }},
    {"field": "Price", "sortable": True},
    {"field": "PriceΔ", "sortable": True, "cellStyle": {
            "styleConditions": [
                {"condition": "params.value < 0", "style": {"color": "#FC766A"}},
                {"condition": "params.value > 0", "style": {"color": "#CCF381"}}
            ]
        }},
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
    {"field": "Premium/Discount", "sortable": True, },
    {"field": "52W NAV Avg", "sortable": True},
    {"field": "52W NAV Low", "sortable": True},
    {"field": "52W NAV High", "sortable": True},
    {"field": "Current Yield", "sortable": True},
    {"field": "Distribution Amount", "sortable": True},
    {"field": "Distribution Frequency", "sortable": True},
    {"field": "Fiscal Year End", "sortable": True, },
]

defaultColDef = {
    "resizable": True,
    "initialWidth": 200,
    "wrapHeaderText": True,
    "autoHeaderHeight": True,
    "sortable": True,
    "filter": True,
}

# Create the AGGrid component
table = dag.AgGrid(
    id='table',
    columnDefs=columnDefs,
    rowData=df.to_dict('records'),
    style = {"height": "1250px", "width": "100%"},  # Set the height attribute here
    columnSize="sizeToFit",
    defaultColDef = defaultColDef,
    dashGridOptions={"autopaginationAutofPageSize":True}
)

external_stylesheets = [
    '/assets/custom.css'  # your custom stylesheet
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    [table],
    style={"margin": 20},)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
