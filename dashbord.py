import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os.path
import geopandas as gp

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG],meta_tags=[{'name':'viewport','content':'width=device-width, initial-scale=1.0'}])

#figure construction
canton_path = os.path.join('Data','Cantons-observation.geojson')

cantons = gp.read_file(canton_path)
cantons.set_index('id')

fig = px.choropleth(data_frame=cantons,geojson=cantons.geometry,locations=cantons.index,color="NUMPOINTS",hover_name="name",hover_data=['NUMPOINTS'],fitbounds='locations',labels={'NUMPOINTS':'Obs'})
fig.update_layout(paper_bgcolor='#000',font_color='#fff',plot_bgcolor='#000',modebar_bgcolor='#000')
fig.update_geos(visible=False)

#stats construction
stat_path = os.path.join('Data','Sorted_Swiss.csv')

statimal = pd.read_csv(stat_path)

statimal = pd.DataFrame(statimal['verbatimScientificName'].value_counts())

reste = 0
dico = (statimal[10:]).to_dict()['verbatimScientificName']
for key in dico:
    reste+= int(dico[key])


statimal = statimal[:10].to_dict()

statimal['verbatimScientificName']['Reste']=reste

statimal = pd.DataFrame(statimal)

statfig = px.pie(data_frame=statimal,values='verbatimScientificName',names=statimal.index)
statfig.update_layout(paper_bgcolor='#000',font_color='#fff')


#Layout of the page
#--------------------------------------------------------------------------------------
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Switzerland by Animals',className='text-center'))

    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='swiss-animals',figure=fig),width={'size':7,'offset':0,'order':1}),
        dbc.Col(dcc.Graph(id='animal-stats',figure=statfig),width={'size':5,'offset':0,'order':2})
    ],no_gutters=True,justify='start'),
    dbc.Row([

    ])
])

#Callback: update
#---------------------------------------------------------------------------------------

# @app.callback(
#     Output(component_id='swiss-animals',component_property='figure')
# )
# def update_graph():

#     file_path = os.path.join('Data','CantonCH.geojson')

#     with open(file_path) as fp:
#         cantons = json.load(fp)

#     fig = px.choropleth(geojson=cantons,locations="id",featureidkey="properties.id")

#     return fig


if __name__ == '__main__':
    app.run_server(debug=True,port=8000)
