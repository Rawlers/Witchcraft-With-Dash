import json
import plotly.express as px
import pandas
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

df = pandas.read_csv("table-2.csv")

fig = px.scatter_geo(df, locations="iso_alpha",
                     hover_name="country", size="count", color_discrete_sequence=['#ff7f0e'],
                     projection="natural earth", size_max=40, title="Executions for Witchcraft per Country")
fig.update_geos(showcountries=True)

fig.update_layout(clickmode='event+select',
                  width=1100,
                  height=700)

app = dash.Dash()

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    dcc.Graph(id = 'basic-interactions', figure=fig, style={'float': 'left', 'margin': 'auto'}),

    html.Div([
        dcc.Markdown("""
        Click on bubbles to display gender distribution
    """),
        html.Pre(id='click-data', style=styles['pre']),
    ], className='three columns', style={'float': 'right', 'margin': 'auto'}),
    ])


@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    country = clickData['points'][0]['location']
    gender_df = pandas.DataFrame(df.loc[df['iso_alpha'] == country])
    gender_df = gender_df.drop(labels=['nationality', 'country', 'continent', 'count', 'iso_alpha'], axis=1)

    values = [gender_df.iloc[0]['male'], gender_df.iloc[0]['female']]
    names = ['Male', 'Female']

    pie_chart = px.pie(gender_df, values=values, names=names, color_discrete_sequence=['red', 'blue'])
    pie_chart.update_layout(height=400, width=400)

    return dcc.Graph(figure=pie_chart)



if __name__ == '__main__':
    app.run_server(debug=True)

