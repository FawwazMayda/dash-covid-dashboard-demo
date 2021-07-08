import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json

#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
def filter_df(df):
    df = df[~df.location.isin(df.continent.unique())]
    df = df[~df.location.isin(['World'])]
    df.loc[df.location == 'United States','location'] = 'United States of America'
    return df

def read_geojson(str_file):
    with open(str_file) as f:
        geo_json = json.load(f)
    return geo_json

def get_df_for_map(df):
    grouped = pd.DataFrame(df.groupby('location')['new_cases'].sum()).reset_index()
    return grouped

url_to_download = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url_to_download)
df = filter_df(df)
geo_json = read_geojson('countries.geojson')

app = dash.Dash()
server = app.server

figure = px.choropleth(get_df_for_map(df),geojson=geo_json,locations='location',color='new_cases',featureidkey='properties.ADMIN',color_continuous_scale='reds')
figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div([
    html.H1("Dash Covid 19 Dashboard on Heroku"),
    dcc.Graph(id='graf',figure=figure)
])

if __name__ == "__main__":
    app.run_server(debug=True)