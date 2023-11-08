import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
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
                        "sideBar": sidebarDef,
                        "animateRows": True, 
                        "skipHeaderOnAutoSize": True,                                          
        },
        enableEnterpriseModules= True,
    )

    return table

# Initialize Dash app with external stylesheets if needed
external_stylesheets = [
    '/custom.css'  # your custom stylesheet
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Store(id='last-clicked-button', storage_type='session'),

    html.Div(id='navbar', style={'display': 'flex', 'justify-content': 'center', 'gap': '10px'}, children=[
        html.Button('CEF Dashboard', id='btn-cefs', n_clicks=0),
        html.Button('Research Center', id='btn-researchcenter', n_clicks=0),
        html.Button('Page 1', id='btn-page1', n_clicks=0),
        html.Button('Page 2', id='btn-page2', n_clicks=0),
        html.Button('Page 3', id='btn-page3', n_clicks=0),
    ]),
    
    html.Div(id='content', style={'padding-top': '50px'}),
])

@app.callback(
    [Output('last-clicked-button', 'data'),
     Output('content', 'children')],
    [Input('btn-researchcenter', 'n_clicks'),
     Input('btn-cefs', 'n_clicks'),    
     Input('btn-page1', 'n_clicks'),
     Input('btn-page2', 'n_clicks'),
     Input('btn-page3', 'n_clicks')],
    [State('last-clicked-button', 'data')]
)

def update_content(n_dashboard, n_pdf, n_page1, n_page2, n_page3, last_clicked):
    ctx = dash.callback_context
    button_id = ctx.triggered_id or last_clicked

    if button_id == 'btn-cefs':
        # Replace generate_dashboard() with the actual function that generates the dashboard
        return 'btn-cefs', generate_dashboard()
    elif button_id == 'btn-researchcenter':
    # Combine PDFs and podcasts in one layout
        return 'btn-researchcenter', html.Div([
    # Podcasts side by side
    html.Div([
        html.Iframe(
            src="https://open.spotify.com/embed/show/1T6xOGR2S5tY6bZ7XbpAC3?utm_source=generator&theme=0",
            width="35%",
            height="100px",
        ),
        html.Iframe(
            src="https://open.spotify.com/embed/show/48EaweC3xjFdgfg2XAMMLX?utm_source=generator",
            width="35%",
            height="100px",
        ),
        html.Iframe(
            src="https://open.spotify.com/embed/show/0f4MGmaXmzedzoqm4P5aXd?utm_source=generator",
            width="35%",
            height="100px",
        ),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    # PDFs side by side below the podcasts
    html.Div([
        html.Iframe(
            src="https://share.refinitiv.com/assets/newsletters/Morning_News_Call/MNC_US.pdf",
            width="50%",
            height="750px",
        ),
        html.Iframe(
            src="https://share.refinitiv.com/assets/newsletters/The_Day_Ahead/TDA_NAM.pdf",
            width="50%",
            height="750px",
        ),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'padding-top': '2px'}),
])

    elif button_id == 'btn-page1':
        # Add content for Page 1
        return button_id, html.Div([])  # Update with Page 1 content
    elif button_id in ['btn-page2', 'btn-page3']:
        # Add content for Page 2 and Page 3
        return button_id, html.Div([])  # Update with Page 2 and Page 3 content
    
    # Default return statement if no buttons have been clicked
    return last_clicked, html.Div([])  # Update with default content

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
