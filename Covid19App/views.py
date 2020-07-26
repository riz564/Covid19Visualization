import itertools

from django.shortcuts import render
import requests

import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go
from collections import deque
import io
import collections
import os


# Create your views here.


def plotWorldMap(df):
    fig = go.Figure(data=go.Choropleth(
        locations=df['Country'],
        locationmode='country names',
        z=df['TotalConfirmed'],
        colorscale='Reds',
    ))

    fig.update_layout(
        title_text='Confirmed Cases as of Today, 2020',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    return fig


def plotPieMap(df):
    fig = px.pie(df, values='TotalConfirmed', names='Country', height=600)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.update_layout(
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=False,
        ))

    return fig


def plotBarMap(df1):
    df1 = df1.groupby(['Country', 'Date'])['Confirmed', 'Deaths', 'Recovered'].sum().reset_index().sort_values(
        'Date', ascending=True)
    fig = px.bar(df1, x="Date", y="Confirmed", color='Country', text='Confirmed', orientation='v',
                 height=600,
                 title='Cases')
    return fig
    '''if typemap == 'Death':
        fig = px.bar(bar_data, x="Date", y="TotalDeaths", color='Country', text='Deaths', orientation='v', height=600,
                     title='Deaths')
        return fig
    if typemap == 'Recovered':
        fig = px.bar(bar_data, x="Date", y="TotalRecovered", color='Country', text='Recovered', orientation='v',
                     height=600,
                     title='Recovered')
        return fig'''


def index(request):
    data = True
    result = None
    globalSummary = None
    countries = None
    worldmap = None
    deathmap = None
    piemap = None
    confirmedmap = None
    recoveredmap = None
    while data:
        try:
            fieldnames = []
            result = requests.get('https://api.covid19api.com/summary')
            #result1 = requests.get('https://api.covid19api.com/all')
            URL_DATASET = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
            #print(result1)
            globalSummary = result.json()['Global']
            countries = result.json()['Countries']
            #allData = result1.json()
            data = False
            #dfAllData = pd.DataFrame(allData)
            df = pd.DataFrame(countries)
            dfAllData = pd.read_csv(URL_DATASET)
            print(dfAllData.head(7))
            fig = plotWorldMap(df)
            worldmap = plot(fig, output_type='div')
            fig = plotPieMap(df)
            piemap = plot(fig, output_type='div')
            fig = plotBarMap(dfAllData)
            confirmedmap = plot(fig, output_type='div')
            # deathfig = plotBarMap(df, 'Death')
            # deathmap = plot(deathfig, output_type='div')
            # recovredfig = plotBarMap(df, 'Recovered')
            # recoveredmap = plot(recovredfig, output_type='div')



        except:
            data = True
    return render(request, 'index.html',
                  {'globalSummary': globalSummary, 'countries': countries,
                   'worldmap': worldmap, 'piemap': piemap,
                   'confirmedmap': confirmedmap, 'deathmap': deathmap,
                   'recoveredmap': recoveredmap})
