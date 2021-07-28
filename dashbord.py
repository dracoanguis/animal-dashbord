import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from pandas._config import config
import plotly.express as px
import os.path
import geopandas as gp
import json
import update_general_data as ugd

#check data 
ugd.checkSwiss()


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG],meta_tags=[{'name':'viewport','content':'width=device-width, initial-scale=1.0'}])


#stats construction
# stat_path = os.path.join('Data','Sorted_Swiss.csv')

# statimal = pd.read_csv(stat_path)

# statimal = pd.DataFrame(statimal['verbatimScientificName'].value_counts())

# reste = 0
# dico = (statimal[10:]).to_dict()['verbatimScientificName']
# for key in dico:
#     reste+= int(dico[key])


# statimal = statimal[:10].to_dict()

# statimal['verbatimScientificName']['Other species']=reste

# statimal = pd.DataFrame(statimal)

# statfig = px.pie(data_frame=statimal,values='verbatimScientificName',names=statimal.index)
# statfig.update_layout(paper_bgcolor='#000',font_color='#fff',margin={'r':0,'l':0,'t':0,'b':0})

#General variable
CANTONS = ['AG','AI','AR','BE','BL','BS','FR','GE','GL','GR','JU','LU','NE','NW','OW','SG','SH','SO','SZ','TG','TI','UR','VD','VS','ZG','ZH']
CARD_COLOR = '#353232'

mapbox_acess_token = 'pk.eyJ1IjoiZ2FyZ2FuIiwiYSI6ImNrcmdicGV3NzBnNWozMXFuNzUwYXd3eXAifQ.sSL3-o-ywElRud8pRM4NKw'
mapbox_style_url = 'mapbox://styles/gargan/ckrgedfau5bc417o52w9owh1g'

MAP_COLOR_SCHEME = [[0,'#fff6c'],[0.125,'#f6e035'],[0.25,'#e79522'],[0.375,'#cb2f2b'],[0.5,'#910003'],[0.625,'#5e0000'],[0.75,'#340000'],[0.825,'#a74694']]


#Layout of the page
#--------------------------------------------------------------------------------------
app.layout=dbc.Container([
    dbc.Row( #title row
        dbc.Col(
			dbc.Card(
				dbc.CardBody(
					[
						html.H5('Fluffboard - human-animal interactions with consideration of population density',
						className='card-title',
						),
						html.H6('Evaluations based on the reporting data from GBIF and iNaturalist',
						className='card-subtitle'
						)
					],
				),
				id='title-Card',
				className='text-white w-150',
				color=CARD_COLOR,
				style={'width':'90vw'}
			),
			className='m-2 px-5',
		),
    ),
    dbc.Row([ #body row
        dbc.Col( #Left column
			[
				dbc.Row( #Map location
					dbc.Col(
						dbc.Card(
							dcc.Graph(
								id='swiss-map',
								figure={},
								className='m-1',
								style={'height':'50vh'},
								config=dict(
									doubleClick='reset'
								)
							),
							color=CARD_COLOR,
							className='m-1'
						),
						width={'size':11,'offset':0}
					),
					no_gutters=True,
					justify='center'
				),
				dbc.Row( #Counts location
					dbc.Col(
						dbc.Card(
							'blip blop blorp',
							className='m-1'
						),
						width={'size':11,'offset':0}
					),
					no_gutters=True,
					justify='center'
				)
			],
			width=7,
			className='align-content-right',
			style={'margin-left':'0px','margin-right':'0px'},
			align='start'
		),
        dbc.Col( #right column
			[
				dbc.Row( #filters location
					dbc.Col(
						dbc.Card(
							[
								dbc.CardHeader(
									html.H6('Population selector'),
									className='text-white'
								),
								dbc.CardBody(
									[
										dcc.Slider(
											id='population-slider',
											step=None,
											min=0,
											max=1000,
											value=0,
											marks={
												num:{
													'label':str(num),
													'style':{'color':'white'}
												}
												for num in [x*100 for x in range(0,11)]
											}
										)
									],
									className='m-0'
								)
							],
							className='m-1',
							color=CARD_COLOR,
							style={'height':'16vh'}
						),
						width={'size':11,'offset':0}
					),
					no_gutters=True
				),
				dbc.Row( #pie chart proportion location
					dbc.Col(
						dbc.Card(
							[
								dbc.CardHeader(
									html.H6('Proportion of animals by species in Switzerland',
										id='pie-title',
										className='text-white')
								),
								dbc.CardBody(
									dcc.Graph(
										id='animal-proportion',
										figure={},
										className='m-0',
										style={'height':'21vh'}
									)
								)
							],
							className='m-1',
							color=CARD_COLOR,
							style={'height':'32vh'}
						),
						width={'size':11,'offset':0}
					),
					no_gutters=True,
					justify='start'
				),
				dbc.Row( #Bar chart number proportion
					dbc.Col(
						dbc.Card(
							[
								dbc.CardHeader(
									html.H6('Number of animals by species',className='text-white')
								),
								dbc.CardBody(
									dcc.Graph(
										id='animal-number',
										figure={},
										className='m-1',
										style={'height':'21vh'}
									)
								)
							],
							className='m-1',
							style={'height':'32vh'},
							color=CARD_COLOR
						),
						width={'size':11,'offset':0}
					),
					no_gutters=True
				)
			],
			width=5,
			style={'margin-left':'0px','margin-right':'0px'}
		)
    ],no_gutters=True,
	),
],fluid=True,className='mr-0 ml-0')

#Callback: update
#---------------------------------------------------------------------------------------

@app.callback(
	Output('swiss-map','figure'),
	Input(component_id='population-slider',component_property='value'),
)
def update_swiss_map(pop):

	sip = os.path.join('Data','swissInfo.csv')
	smp = os.path.join('Data','CantonsCh.geojson')

	with open(smp,'r') as fp:
		cantons = json.load(fp)

	infos = pd.read_csv(sip,)
	infos.set_index('id',inplace=True)

	fig = dict(
		data=
			[
			dict(
				type='choroplethmapbox', # type of data
				geojson=cantons,
				featureidkey='properties.id', # place where the id of a feature is fetched
				locations=[cantons['features'][x]['properties']['id'] for x in range(26)],
				z=[(infos[('pop'+str(pop))]).loc[x] for x in ([cantons['features'][x]['properties']['id'] for x in range(26)])],
				showscale=False, #hide the atrocious colorbar legend
				hovertext=[cantons['features'][x]['properties']['name'] for x in range(26)],
				colorscale=MAP_COLOR_SCHEME # colorscale wich was determined on the other thing	
			)
		],
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
				zoom=6.3
			),
			autosize=True,
			clickmode='event',
			annotations=[
				dict(
					showarrow=False,
					x=0.98,
					y=0.10,
					text='Reset',
					captureevents=True,
					bgcolor='#2d3c48',
					font=dict(
						color='white'
					)
				)
			]
		)
	)

	return fig

@app.callback(
	[
		Output('animal-proportion','figure'),
		Output('pie-title','children'),
		Output('swiss-map','clickAnnotationData')
	],
	[
		Input('swiss-map','clickData'),
		Input('population-slider','value'),
		Input('swiss-map','clickAnnotationData')
	]
)
def update_animal_proportion(clicked,pop,clickanno):
	print(clicked)
	print(clickanno)

	if clicked is None or clickanno is not None:
		tocount = pd.DataFrame()
		for ctid in CANTONS:
			fp = os.path.join('Data','cantonInfo',(str(ctid)+'.csv'))
			df = pd.read_csv(fp)
			df = df[df['populationDensity']>=pop]
			tocount = tocount.append(df,ignore_index=False)
	
		statimal = tocount['class'].value_counts()

		fig = px.pie(
			data_frame=statimal,
			names=statimal.index,
			values='class',
		)

		#To hide percentage
		fig.update_traces(textposition='inside')
		fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

		fig.update_layout(
			paper_bgcolor=CARD_COLOR,
			font_color='#fff',
			margin={'r':0,'l':0,'t':0,'b':0},
			showlegend=False,
		)

		return fig, 'Proportion of animals by class in Switzerland', None

	ctid = clicked['points'][0]['location']
	ctname = clicked['points'][0]['hovertext']

	fp = os.path.join('Data','cantonInfo',(str(ctid)+'.csv'))
	df = pd.read_csv(fp)
	df = df[df['populationDensity']>=pop]
	
	statimal = df['class'].value_counts()

	fig = px.pie(
		data_frame=statimal,
		names=statimal.index,
		values='class',
	)

	#To hide percentage
	fig.update_traces(textposition='inside')
	fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

	fig.update_layout(
		paper_bgcolor=CARD_COLOR,
		font_color='#fff',
		margin={'r':0,'l':0,'t':0,'b':0},
		showlegend=False,
	)

	title = 'Proportion of animals by class in {}'.format(ctname)

	return fig, title, None


if __name__ == '__main__':
    app.run_server(debug=True,port=8000)
