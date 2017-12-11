# Import a CSV file with the data

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('Data.csv')

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['UNIT'].unique()
available_geo = df['GEO'].unique()

# We create the first graph

app.layout = html.Div([

    html.Div([
        html.H1(children='Scatter Plot',style={'text-align':'center','font-family':'monospace'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Chain linked volumes, index 2010=100'
                ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Current prices, million euro'
                ),
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic'),

        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=2007,
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}
        )
    ]),


    #We create the second graph


    html.Div([
        html.H1(children='Line Chart',style={'margin-top':'5%','text-align':'center','font-family':'monospace'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='indicator-select',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Current prices, million euro'
                ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='country-select',
                    options=[{'label': i, 'value': i} for i in available_geo],
                    value='Norway'
                ),
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),
        dcc.Graph(id='indicator-graphic2'),
    ])
    #END SECOND
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, year_value):
    dff = df[df['TIME'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['UNIT'] == xaxis_column_name]['Value'],
            y=dff[dff['UNIT'] == yaxis_column_name]['Value'],
            text=dff[dff['UNIT'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 10,
                'color':'rgb(22, 96, 167)',
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
#CALLBACK SECOND GRAPH
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('indicator-select', 'value'),
     dash.dependencies.Input('country-select', 'value'),])
def update_graph(indicator_name, country_name):
    dff = df[df['GEO'] == country_name]

    return {
        'data': [go.Scatter(
            x=dff[dff['UNIT'] == indicator_name]['TIME'],
            y=dff[dff['UNIT'] == indicator_name]['Value'],
            text=dff[dff['UNIT'] == indicator_name]['Value'],
            mode='lines',
            line = dict(
                color = ('rgb(22, 96, 167)'),
                width = 4,)
        )],
        'layout': go.Layout(
            xaxis={
                'title': country_name,
            },
            yaxis={
                'title': indicator_name,
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
