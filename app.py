import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import html, dcc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd

from urllib.parse import unquote

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

exams = pd.read_csv('https://raw.githubusercontent.com/raeeschaudhary/coursera_test/main/exams.csv')
overall = (exams.math_score + exams.reading_score + exams.writing_score)/3
exams["overall"] = overall

def make_empty_fig():
    fig = go.Figure()
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.plot_bgcolor = '#E5ECF6'
    return fig

main_layout = html.Div([
    html.Div([
    dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Distribution", href="dist")),
        dbc.NavItem(dbc.NavLink("References", href="refer")),
    ],
    brand="Student Performance - Data Visualization",
    brand_href="/",
    color="primary",
    dark=True,
    ),
    dbc.NavbarSimple([
        ]),
    dcc.Location(id='location'),
    html.Div(id='main_content'),
    html.Br(),
]),
    html.Br(),
],  style={'backgroundColor': '#E5ECF6'})

main_dashboard = html.Div([
        dbc.Row([
            dbc.Col(lg=1),
            dbc.Col([
                    dbc.Label('Differentiating Variable'),
                    html.Br(),
                    dcc.Dropdown(id='diff_dropdown',
                         value='gender', options=[{'label': v, 'value': v} 
                                                  for v in ['gender', 'ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']]),
                ], md=12, lg=4),
                dbc.Col([
                    dbc.Label('Score to Compare'),
                    dcc.Dropdown(id='ques_dropdown',
                         value='math_score',
                         options=[{'label': v, 'value': v}
                                  for v in ['math_score', 'reading_score', 'writing_score', 'overall']]),
                ], md=12, lg=3),
                dbc.Col([
                    dbc.Label('Compare Score Against'),
                    dcc.Dropdown(id='comp_dropdown',
                         value='overall',
                         options=[{'label': v, 'value': v}
                                  for v in ['math_score', 'reading_score', 'writing_score', 'overall']]),
                ], md=12, lg=3),
        ], style={'backgroundColor': '#E5ECF6'}),
        dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Filter Education of Parents'),
            dcc.Dropdown(id='edu_selector',
                         multi=True,
                         placeholder='Select one or more',
                         options=[{'label': edu, 'value': edu}
                                  for edu in exams['parental_level_of_education'].drop_duplicates().sort_values()]), 
            
            dcc.Graph(id='comparison_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
        dbc.Col([
            dbc.Label('Filter Ethnicity'),
            dcc.Slider(1, 6, step=None, id='ethnicity_slider',
                       marks={
                           1: 'Group A',
                           2: 'Group B',
                           3: 'Group C',
                           4: 'Group D',
                           5: 'Group E',
                           6: "All"
                       },
                       value=6
                      ),
            dcc.Graph(id='heatmap_graph',
                      figure=make_empty_fig()),
            html.Br(),
            ], md=12, lg=5),
        ]),    
], style={'backgroundColor': '#E5ECF6'})

dist_dashboard = html.Div([
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Filter Education of Parents'),
            dcc.Dropdown(id='edu_selector1',
                         multi=True,
                         placeholder='Select one or more',
                         options=[{'label': edu, 'value': edu}
                                  for edu in exams['parental_level_of_education'].drop_duplicates().sort_values()]),
            html.Br(),
            dcc.Graph(id='gender_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='parental_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='test_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='read_dist_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
        dbc.Col([ 
            dbc.Label('Filter Ethnicity'),
            dcc.Slider(1, 6, step=None, id='ethnicity_slider1',
                       marks={
                           1: 'Group A',
                           2: 'Group B',
                           3: 'Group C',
                           4: 'Group D',
                           5: 'Group E',
                           6: "All"
                       },
                       value=6
                      ),
            html.Br(),
            dcc.Graph(id='ethnicity_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='lunch_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='math_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='write_dist_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
            
    ]),
    
], style={'backgroundColor': '#E5ECF6'})

refer_dashboard = html.Div([
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            html.H1('References'),
            ], md=12, lg=5),
        dbc.Col([
            
        ], md=12, lg=5),
    ]),
])

app.validation_layout = html.Div([
    main_layout,
    main_dashboard,
    dist_dashboard,
    refer_dashboard,
])


app.layout = main_layout

def filter_data(edu_levels, ethnicity, filtered):
    group = ""
    if edu_levels:
        filtered = filtered[filtered['parental_level_of_education'].isin(edu_levels)]
    if ethnicity == 1:
        group = 'group A'
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 2:
        group = "group B"
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 3:
        group = "group C"
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 4:
        group = "group D"
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 5:
        group = "group E"
        filtered = filtered[filtered['ethnicity'] == group]
    else:
        group = ""
    return filtered

#this method updates the layout to order and main 
@app.callback(Output('main_content', 'children'),
              Input('location', 'pathname'))
def display_content(pathname):
    if unquote(pathname[1:]) in ['dist']:
        return dist_dashboard
    elif unquote(pathname[1:]) in ['refer']:
        return refer_dashboard
    else:
        return main_dashboard
    
#This method plots the main figures with input from user
@app.callback(Output('comparison_graph', 'figure'),
              Output('heatmap_graph', 'figure'),
              Input('edu_selector', 'value'),
              Input('ethnicity_slider', 'value'),
              Input('diff_dropdown', 'value'),
              Input('ques_dropdown', 'value'),
             Input('comp_dropdown', 'value'))
def display_main(edu_levels, ethnicity, diff, ques, comp):
    filtered = exams.copy()
    filtered = filter_data(edu_levels, ethnicity, filtered)
    fig1 = px.scatter(filtered, x=ques, y=comp, color=diff, hover_data=[diff], trendline="ols")
    cols = ['math_score', 'reading_score', 'writing_score', 'overall']
    df_corr = filtered[cols].corr().round(2)
    fig2 = go.Figure()
    fig2.add_trace(go.Heatmap(x = df_corr.columns, y = df_corr.index, z = np.array(df_corr)))
    return fig1, fig2

#This method plots the main figures with input from user
@app.callback(Output('gender_dist_graph', 'figure'),
              Output('ethnicity_dist_graph', 'figure'),
              Output('parental_dist_graph', 'figure'),
              Output('lunch_dist_graph', 'figure'),
              Output('test_dist_graph', 'figure'),
              Output('math_dist_graph', 'figure'),
              Output('read_dist_graph', 'figure'),
              Output('write_dist_graph', 'figure'),
              Input('edu_selector1', 'value'),
              Input('ethnicity_slider1', 'value'),
             )
def display_dist(edu_levels, ethnicity):
    filtered = exams.copy()
    filtered = filter_data(edu_levels, ethnicity, filtered)
    fig1 = px.histogram(filtered, x="gender", color="gender", labels={'gender':'Gender'}, title='Gender Distribution')
    fig2 = px.histogram(filtered, x="ethnicity", color="ethnicity", labels={'ethniciy':'Ethniciy/Race'}, title='Ethnicity/Race Distribution (Filter)')
    fig3 = px.histogram(filtered, x="parental_level_of_education", color="parental_level_of_education", 
                        labels={'parental_level_of_education':'Parental Level of Education'}, 
                        title='Parental Level of Education Distribution (Filter)')
    fig4 = px.histogram(filtered, color="lunch", x="lunch", labels={'lunch':'Lunch Program'}, title='Lunch Program Distribution')
    fig5 = px.histogram(filtered, x="test_preparation_course", color="test_preparation_course", 
                        labels={'test_preparation_course':'Test Preparation Course'}, 
                        title='Test Preparation Distribution')
    fig6 = px.histogram(filtered, x="math_score", labels={'math_score':'Math Score'}, title='Math Score Distribution')
    fig7 = px.histogram(filtered, x="writing_score", labels={'writing_score':'Writing Score'}, title='Writing Score Distribution')
    fig8 = px.histogram(filtered, x="reading_score", labels={'reading_score':'Reading Score'}, title='Reading Score Distribution')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8

    
if __name__ == '__main__':
    app.run_server(debug=True)