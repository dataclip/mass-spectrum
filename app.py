import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('test_data.csv', sep = '\t')

energy_values = df.columns[1:]

app.layout = html.Div([
    html.Div([
        html.H4('Plot mass spectrum & and corresponding PIE curve'),
        html.Div([
            html.H6('Select an energy value'),

            dcc.Dropdown(
                id='energy-value',
                options=[{'label': i, 'value': i} for i in energy_values],
                value = energy_values[0],
                placeholder="Select an energy value to plot mass spectrum",
            ),
           
        ],
        style={'width': '35%', 'display': 'inline-block'}),

    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='mass-spectrum',
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='pie-curve'),
    ], style={'display': 'inline-block', 'width': '49%'}),

])


@app.callback(
    dash.dependencies.Output('mass-spectrum', 'figure'),
    [dash.dependencies.Input('energy-value', 'value'),
     ])

def update_graph(energy_value):
    
    fig =  px.line(x=df['Energy'], y=df[energy_value])
    fig.update_layout(
    title="Mass Spectrum at " + energy_value + " eV",
    xaxis_title="m/z",
    yaxis_title="Intensity",
    )

    return fig


@app.callback(
    dash.dependencies.Output('pie-curve', 'figure'),
    [dash.dependencies.Input('mass-spectrum', 'hoverData'),
     ])


def update_pie_curve(hoverData):
    # print(df.head())
    points_dict = hoverData['points'][0]
    x_value = points_dict.get('x')
    print(points_dict.get('x'))
    dff = df[df['Energy'] == x_value].T
    # print(dff.head())

    dff = dff.iloc[1:]
    dff = pd.DataFrame(dff)
    # dff = dff.T
    dff.columns = ['Intensity']
    print(dff.head())
    fig = px.line(x=dff.index, y=dff['Intensity'])
    fig.update_layout(
    title="PIE curve of mass " + str(x_value),
    xaxis_title="energy (eV)",
    yaxis_title="Intensity",
    )
 
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
