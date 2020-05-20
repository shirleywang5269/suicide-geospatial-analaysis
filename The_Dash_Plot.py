#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_colorscales
import pandas as pd
import cufflinks as cf
import numpy as np
import re

# app = dash.Dash(__name__)
# server = app.server


app = dash.Dash(
    __name__,
    assets_external_path='https://codepen.io/plotly/pen/EQZeaW.css'
)
app.scripts.config.serve_locally = False


# In[ ]:





# In[2]:


df_full_data_1 = pd.read_csv(r'suicide2009-2013.txt', sep='\t')
df_full_data_1.tail()
df_full_data_2 = pd.read_csv(r'suicide2014-18.txt', sep='\t')
df_full_data_2.tail()
frames=[df_full_data_1,df_full_data_2]
df_full_data = pd.concat(frames)
# pd.set_option('display.max_rows', df_full_data.shape[0]+1)
df_full_data.head()


# In[3]:


# min(df_full_data["Age Adjusted Rate"])


# In[4]:


import pandas as pd
test=pd.read_csv("age_adjusted_death_rate_suicide.csv")
df_2013 = test[(test.Year == 2013)]
BINS = df_2013['binned'].unique()
test.head()


# In[5]:


# df_lat_lon.__dict__


# In[6]:


# df_lat_lon['Latitude ']


# In[7]:


# -*- coding: utf-8 -*-

df_lat_lon = pd.read_csv('lat_lon_counties.csv')
print(type(df_lat_lon))

# print(df_lat_lon)
df_lat_lon['FIPS '] = df_lat_lon['FIPS '].apply(lambda x: str(x).zfill(5))
print(df_lat_lon[:5])
for col in df_lat_lon.columns:
    df_lat_lon[col] = df_lat_lon[col].astype(str)
    
df_lat_lon['description'] = df_lat_lon['FIPS '] + df_lat_lon['Population(2010)']+ '<br>' + 'Population(2010) ' + df_lat_lon['Population(2010)'] + ' TotalAreakm2 ' + df_lat_lon['TotalAreakm2 '] + '<br>' 

print(df_lat_lon[:5])


# In[ ]:





# In[8]:


df_full_data['County Code'] = df_full_data['County Code'].apply(lambda x: str(x).zfill(5))

YEARS = [2009,2010,2011,2012,2013]

# BINS = ['0-2', '2.1-4', '4.1-6', '6.1-8', '8.1-10', '10.1-12', '12.1-14', \
# 		'14.1-16', '16.1-18', '18.1-20', '20.1-22', '22.1-24',  '24.1-26', \
# 		'26.1-28', '28.1-30', '>30']


DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", 	"#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", 	"#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]

DEFAULT_OPACITY = 0.8

DEFAULT_COLORSCALE = list(reversed(DEFAULT_COLORSCALE))

mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

# df_full_data


# In[ ]:





# In[9]:


'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''

app.layout = html.Div(children=[

	html.Div([
		html.Div([
			html.Div([
                #Title
				html.H4(children='Rate of US Suicide Deaths'),
				html.P('Drag the slider to change the year:'),
			]),
                #Define Year
			html.Div([
				dcc.Slider(
					id='years-slider',
					min=min(YEARS),
					max=max(YEARS),
					value=min(YEARS),
					marks={str(year): str(year) for year in YEARS},
				),
			], style={'width':400, 'margin':25}),

			html.Br(),
                #Define Color
			html.P('Map transparency:',
				style={
					'display':'inline-block',
					'verticalAlign': 'top',
					'marginRight': '10px'
				}
			),

			html.Div([
				dcc.Slider(
					id='opacity-slider',
					min=0, max=1, value=DEFAULT_OPACITY, step=0.1,
					marks={tick: str(tick)[0:3] for tick in np.linspace(0,1,11)},
				),
			], style={'width':300, 'display':'inline-block', 'marginBottom':10}),

			html.Div([
				dash_colorscales.DashColorscales(
					id='colorscale-picker',
					colorscale=DEFAULT_COLORSCALE,
					nSwatches=16,
					fixSwatches=True
				)
			], style={'display':'inline-block'}),

			html.Div([
				dcc.Checklist(
				    options=[{'label': 'Hide legend', 'value': 'hide_legend'}],
					labelStyle={'display': 'inline-block'},
                    value=[],
					id='hide-map-legend',
				)
			], style={'display':'inline-block'}),
            
            #Define Zipcode level
			html.Div([
				dcc.Checklist(
				    options=[{'label': 'ZipCode MAP', 'value': 'ZipCode MAP'}],
					labelStyle={'display': 'inline-block'},
                    value=[],
					id='convert_zip_map',
				)
			], style={'display':'inline-block'}),

		], style={'margin':20} ),

		html.P('Heatmap of age adjusted mortality rates \
			from suicide in year {0}'.format(min(YEARS)),
			id = 'heatmap-title',
			style = {'fontWeight':600}
		),

		dcc.Graph(
			id = 'county-choropleth',
			figure = dict(
				data=dict(
					lat = df_lat_lon['Latitude '],
					lon = df_lat_lon['Longitude'],
					text = df_lat_lon['description'],
					type = 'scattermapbox'
				),
				layout = dict(
					mapbox = dict(
						layers = [],
						accesstoken = mapbox_access_token,
						style = 'light',
						center=dict(
							lat=38.72490,
							lon=-95.61446,
						),
						pitch=0,
						zoom=2.5
					)
				)
			)
		),

		html.Div([
			html.P('† Deaths are classified using the International Classification of Diseases, \
				Tenth Revision (ICD–10). Suicide Related deaths are defined as having ICD–10 underlying \
				F01-F99 (Mental and behavioural disorders), \
                F20-F29 (Schizophrenia, schizotypal and delusional disorders), \
                F20 (Schizophrenia) ,F20.4 (Post-schizophrenic depression),\
                F30-F39 (Mood [affective] disorders), F32 (Depressive episode),\
                F32.3 (Severe depressive episode with psychotic symptoms),\
                F40-F48 (Neurotic, stress-related and somatoform disorders),\
                F43 (Reaction to severe stress, and adjustment disorders),\
                F43.1 (Post-traumatic stress disorder),\
                F60-F69 (Disorders of adult personality and behaviour),\
                F60 (Specific personality disorders),\
                F60.3 (Emotionally unstable personality disorder),\
                U00-U99 (Codes for special purposes),\
                U00-U49 (Provisional assignment of new diseases of uncertain etiology),\
                U03 (Terrorism Intentional (Suicide)),\
                V01-Y89 (External causes of morbidity and mortality),\
                X60-X84 (Intentional self-harm).'
			)
		], style={'margin':20})

	], className='six columns', style={'margin':0}),

	html.Div([
		dcc.Checklist(
		    options=[{'label': 'Log scale', 'value': 'log'},
					{'label': 'Hide legend', 'value': 'hide_legend'},
					{'label': 'Include values flagged "Unreliable"', 'value': 'include_unreliable'}],
			labelStyle={'display': 'inline-block'},
			id='log-scale',
            value=[],
			style={'position': 'absolute', 'right': 80, 'top': 10}
		),
		html.Br(),
		html.P('Select chart:', style={'display': 'inline-block'}),
		dcc.Dropdown(
		    options=[{'label': 'Histogram of total number of deaths (single year)', 'value': 'show_absolute_deaths_single_year'},
					{'label': 'Histogram of total number of deaths (2009-2013)', 'value': 'absolute_deaths_all_time'},
					{'label': 'Age-adjusted death rate (single year)', 'value': 'show_death_rate_single_year'},
					{'label': 'Trends in age-adjusted death rate (2009-2013)', 'value': 'death_rate_all_time'}],
			value='show_death_rate_single_year',
			id='chart-dropdown'
		),
		dcc.Graph(
			id = 'selected-data',
			figure = dict(
				data = [dict(x=0, y=0)],
				layout = dict(
					paper_bgcolor = '#F4F4F8',
					plot_bgcolor = '#F4F4F8',
					height = 700
				)
			),
			# animate = True
		)
	], className='six columns', style={'margin':0}),
])


# In[ ]:





# ## CSS STYLE 

# In[ ]:


# app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/EQZeaW.css'})


# ## The backend Function for displaying  map

# In[10]:


@app.callback(
		Output('county-choropleth', 'figure'),
		[Input('years-slider', 'value'),
		Input('opacity-slider', 'value'),
		Input('colorscale-picker', 'colorscale'),
		Input('hide-map-legend', 'value')],
		[State('county-choropleth', 'figure')])
def display_map(year, opacity, colorscale, map_checklist, figure):
	cm = dict(zip(BINS, colorscale))

	data = [dict(
		lat = df_lat_lon['Latitude '],
		lon = df_lat_lon['Longitude'],
		text = df_lat_lon['description'],
		type = 'scattermapbox',
		hoverinfo = 'text',
		#selected = dict(marker = dict(opacity=1)),
		#unselected = dict(marker = dict(opacity = 0)),
		marker = dict(size=5, color='white', opacity=0)
	)]

	annotations = [dict(
		showarrow = False,
		align = 'right',
		text = '<b>Age-adjusted death rate<br>per county per year</b>',
		x = 0.95,
		y = 0.95,
	)]

	for i, bin in enumerate(reversed(BINS)):
		color = cm[bin]
		annotations.append(
			dict(
				arrowcolor = color,
				text = bin,
				x = 0.95,
				y = 0.85-(i/20),
				ax = -60,
				ay = 0,
				arrowwidth = 5,
				arrowhead = 0,
				bgcolor = '#EFEFEE'
			)
		)

	if 'hide_legend' in map_checklist:
		annotations = []

	if 'layout' in figure:
		lat = figure['layout']['mapbox']['center']['lat']
		lon = figure['layout']['mapbox']['center']['lon']
		zoom = figure['layout']['mapbox']['zoom']
	else:
		lat = 38.72490,
		lon = -95.61446,
		zoom = 2.5

	layout = dict(
		mapbox = dict(
			layers = [],
			accesstoken = mapbox_access_token,
			style = 'light',
			center=dict(lat=lat, lon=lon),
			zoom=zoom
		),
		hovermode = 'closest',
		margin = dict(r=0, l=0, t=0, b=0),
		annotations = annotations,
		dragmode = 'lasso'
	)

	base_url = 'https://raw.githubusercontent.com/shirleywang5269/CDCSuicide/master/'
	for bin in BINS:
		geo_layer = dict(
			sourcetype = 'geojson',
			source = base_url + str(year) + '/' + bin + '.geojson',
			type = 'fill',
			color = cm[bin],
			opacity = opacity
		)
		layout['mapbox']['layers'].append(geo_layer)

	fig = dict(data=data, layout=layout)
	return fig


# In[ ]:





# In[11]:


@app.callback(
	Output('heatmap-title', 'children'),
	[Input('years-slider','value')])
def update_map_title(year):
	return 'Heatmap of age adjusted mortality rates 				from suicide in year {0}'.format(year)
@app.callback(
	Output('selected-data', 'figure'),
	[Input('county-choropleth', 'selectedData'),
	Input('log-scale', 'value'),
	Input('chart-dropdown', 'value'),
	Input('years-slider', 'value')])
def display_selected_data(selectedData, checklist_values, chart_dropdown, year):
	print(chart_dropdown)
	print('FIRE SELECTION')
	if selectedData is None:
		print('SelectedData is None')
		return dict(
			data = [dict(x=0, y=0)],
			layout = dict(
				title='Click-drag on the map to select counties',
				paper_bgcolor = '#F4F4F8',
				plot_bgcolor = '#F4F4F8'
			)
		)
	pts = selectedData['points']
	fips = [str(pt['text'].split('<br>')[-1]) for pt in pts]
	for i in range(len(fips)):
		if len(fips[i]) == 4:
			fips[i] = '0' + fips[i]
	print('FIPS', '\n', fips)
	dff = df_full_data[df_full_data['County Code'].isin(fips)]
	dff = dff.sort_values('Year')

	if 'include_unreliable' in checklist_values:
		dff['Age Adjusted Rate'] = dff['Age Adjusted Rate'].str.strip('(Unreliable)')
	else:
		regex_pat = re.compile(r'Unreliable', flags=re.IGNORECASE)
		dff['Age Adjusted Rate'] = dff['Age Adjusted Rate'].replace(regex_pat, 0)

	if chart_dropdown != 'death_rate_all_time':
		title = 'Absolute deaths per county, <b>1999-2016</b>'
		AGGREGATE_BY = 'Deaths'
		if 'show_absolute_deaths_single_year' == chart_dropdown:
			dff = dff[dff.Year == year]
			title='Absolute deaths per county, <b>{0}</b>'.format(year)
		elif 'show_death_rate_single_year' == chart_dropdown:
			dff = dff[dff.Year == year]
			title='Age-adjusted death rate per county, <b>{0}</b>'.format(year)
			AGGREGATE_BY = 'Age Adjusted Rate'

		dff[AGGREGATE_BY] = pd.to_numeric(dff[AGGREGATE_BY], errors='coerce')
		deaths_or_rate_by_fips = dff.groupby('County')[AGGREGATE_BY].sum()
		deaths_or_rate_by_fips = deaths_or_rate_by_fips.sort_values()
		# Only look at non-zero rows:
		deaths_or_rate_by_fips = deaths_or_rate_by_fips[deaths_or_rate_by_fips > 0]
		fig = deaths_or_rate_by_fips.iplot(
			kind='bar',
			y=AGGREGATE_BY,
			title=title,
			asFigure=True)
		fig['layout']['margin']['b'] = 300
		fig['data'][0]['text'] = deaths_or_rate_by_fips.values.tolist(),
		# TODO: Why doesn't the text show up over the bars?
		fig['data'][0]['textposition'] = 'outside',
		if 'log' in checklist_values:
			fig['layout']['yaxis']['type'] = 'log'
		return fig

	fig = dff.iplot(
		kind = 'area',
		x = 'Year',
		y = 'Age Adjusted Rate',
		text = 'County',
		categories = 'County',
		colors = ["#1b9e77","#d95f02","#7570b3","#e7298a","#66a61e",\
					"#e6ab02","#a6761d","#666666","#1b9e77"],
		vline=[year],
		asFigure=True)

	for i, trace in enumerate(fig['data']):
		trace['mode'] = 'lines+markers'
		trace['marker']['size'] = 4
		trace['marker']['line']['width'] = 1
		trace['type']='scatter'
		if 'textformat' in fig['data'][i]:
			del fig['data'][i]['textformat']
		if 'textfont' in fig['data'][i]:
			del fig['data'][i]['textfont']
		fig['data'][i] = trace

	# Only show first 500 lines
	fig['data'] = fig['data'][0:500]

	# See plot.ly/python/reference
	fig['layout']['yaxis']['title'] = 'Age-adjusted death rate per county per year'
	fig['layout']['xaxis']['title'] = ''
	fig['layout']['yaxis']['fixedrange'] = True
	fig['layout']['xaxis']['fixedrange'] = False
	fig['layout']['margin'] = dict(t=50, r=150, b=20, l=80)
	if 'log' in checklist_values:
		fig['layout']['yaxis']['type'] = 'log'
	if 'hide_legend' in checklist_values:
		fig['layout']['showlegend'] = False
		fig['layout']['margin']['r'] = 10
	fig['layout']['hovermode'] = 'closest'
	fig['layout']['title'] = '<b>{0}</b> counties selected'.format(len(fips))
	fig['layout']['legend'] = dict(orientation='v')
	fig['layout']['height'] = 800

	if len(fips) > 500:
		fig['layout']['title'] = fig['layout']['title'] + '<br>(only 1st 500 shown)'

	return fig


# In[ ]:





# In[ ]:


if __name__ == '__main__':
	app.run_server(debug=False)


# In[ ]:




