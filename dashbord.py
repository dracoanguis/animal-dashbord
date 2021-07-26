import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from numpy.core.fromnumeric import trace
import pandas as pd
from pandas.core.frame import DataFrame
import plotly.express as px
import os.path
import geopandas as gp
import json

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG],meta_tags=[{'name':'viewport','content':'width=device-width, initial-scale=1.0'}])

#figure construction

canton_source ='https://raw.githubusercontent.com/dracoanguis/animal-dashbord/main/Data/Cantons-observation.geojson?token=ANUIZ2E3OVFR2HEPEXI6M5LA7XZJI'

canton_path = os.path.join('Data','Cantons-observation.geojson')

with open(canton_path,'r') as cp:
	cantons = json.load(cp)

# canton=gp.read_file(canton_path)
# canton.set_index('id')

#fig = px.choropleth(data_frame=cantons,geojson=cantons.geometry,locations=cantons.index,color="NUMPOINTS",hover_name="name",hover_data=['NUMPOINTS'],fitbounds='locations',labels={'NUMPOINTS':'Obs'})
#fig.update_layout(paper_bgcolor='#fff',font_color='#000',plot_bgcolor='#fff',modebar_bgcolor='#fff',margin={'r':0,'l':0,'t':0,'b':0},legend_bgcolor='rgba(0,0,0,0)')
#fig.update_geos(visible=False)

mapbox_acess_token = 'pk.eyJ1IjoiZ2FyZ2FuIiwiYSI6ImNrcmdicGV3NzBnNWozMXFuNzUwYXd3eXAifQ.sSL3-o-ywElRud8pRM4NKw'
mapbox_style_url = 'mapbox://styles/gargan/ckrgedfau5bc417o52w9owh1g'


# maplayers = [dict(
#                 sourcetype='geojson',
#                 source=cantons['features'][0],
#                 type='fill',
#                 color='#000',
# 				opacity=1,
# 				fill=dict(outlinecolor='#afafaf'),
# 				below=""
# 			)]

# tracesChoro = [
# 	dict(
# 		name='cantons',
# 		type='choroplethmapbox',
# 		geojson=cantons,
# 		featureidkey='properties.id',
# 		locations=['ZU','BE','LU'],
# 		z=[10,20,30],
# 		showlegend=False,
# 		hovertext='blop',
		
# 	)
# ]

datafig = [
			# dict(
            #     opacity=1,
            #     fill='toself', #the filling of points
            #     mode='marker', #mode of display
			# 	# hoveron='fill', doesn't work for this type of map
            #     type='scattermapbox', #what define the type of the map and it's properties (making the map print)
            #     text='blip', #hovertext in order
            #     hoverinfo='text', #where to get the hover
            #     lat=[47,47,46], #lat for every point
            #     lon=[8,9,9], #lon for every point
            #     marker=dict(size=5,color='white',opacity=1, hoverinfo='text') #how the marker look
            # ),
            dict(
                type='choroplethmapbox', # type of data
                # trace=tracesChoro, doesn't work
				geojson=cantons,
				featureidkey='properties.id', # place where the id of a feature is fetched
				locations=[cantons['features'][x]['properties']['id'] for x in range(26)],
				z=[cantons['features'][x]['properties']['NUMPOINTS'] for x in range(26)],
				showscale=False, #hide the atrocious colorbar legend
				hovertext=[cantons['features'][x]['properties']['name'] for x in range(26)],
				colorscale=[[0,'#fcc0c0'],[0.5,'#f14170'],[1,'#b1064e']] # colorscale wich was determined on the other thing			
            )
]


fig = dict(
            data=datafig,
            layout=dict(
                        hovermode='closest',
                        paper_bgcolor='#000',
                        font_color='#fff',
                        plot_bgcolor='#000',
                        modebar_bgcolor='#000',
                        margin={'r':0,'l':0,'t':0,'b':0},
                        mapbox=dict(
                                    layers=[],#maplayers,
                                    accesstoken=mapbox_acess_token,
                                    style=mapbox_style_url,
                                    center=dict(lat=46.905,lon=8.258),
                                    pitch=0,
                                    zoom=6.3),
                        autosize=True)
            )


#stats construction
stat_path = os.path.join('Data','Sorted_Swiss.csv')

statimal = pd.read_csv(stat_path)

statimal = pd.DataFrame(statimal['verbatimScientificName'].value_counts())

reste = 0
dico = (statimal[10:]).to_dict()['verbatimScientificName']
for key in dico:
    reste+= int(dico[key])


statimal = statimal[:10].to_dict()

statimal['verbatimScientificName']['Other species']=reste

statimal = pd.DataFrame(statimal)

statfig = px.pie(data_frame=statimal,values='verbatimScientificName',names=statimal.index)
statfig.update_layout(paper_bgcolor='#000',font_color='#fff',margin={'r':0,'l':0,'t':0,'b':0})


#Layout of the page
#--------------------------------------------------------------------------------------
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Switzerland by Animals',className='text-center'))

    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='swiss-animals',figure=fig),width={'size':7,'offset':0,'order':1}),
        dbc.Col(dcc.Graph(id='animal-stats',figure=statfig),width={'size':5,'offset':0,'order':2})
    ],no_gutters=False,justify='start'),
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
