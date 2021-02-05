import mesa
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import matplotlib.pyplot as plt
import os
import contextily as ctx
from collections import deque

import mesa
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

import networkx as nx
import re

def intersections(road):
    df = pd.read_csv('_roads3.csv')
    lijst = df['road'].unique()

    matchers = ['N']
    matching = [s for s in lijst if any(xs in s for xs in matchers)]

    df2 = df[df['name'].str.contains('|'.join(matching))].reset_index().drop('index', axis=1)
    side = df2[df2['road'].str.contains('|'.join(matching))].reset_index().drop('index', axis=1)

    side = side.rename(columns={'chainage':'km'})
    side['model_type'] = 'intersection'

    side['intersection'] = ""
    side['length'] = 4
    side = side[side.road == road].reset_index().drop("index", axis=1)
    n = 0

    for i in side.name:
        wordlist = re.sub("[^\w]", " ",  i).split()
        for j in matching:
            if any(j in s for s in wordlist):
                match = [s for s in wordlist if j in s]
                if len(match) == 2:
                    side.loc[n,'intersection'] = str(match[0] + ', ' + match[1])
                elif len(match) == 3:
                    side.loc[n,'intersection'] = str(match[0] + match[1] + match[2])
                elif len(match)==1:
                    side.loc[n,'intersection'] = match[0]
        n += 1

    side = side[['road','km','length','lat','lon','model_type','intersection',]]
        
    return side

def model_structure(road):
    df= pd.read_csv('CandV_Bridges.csv')
    df['model_type'] = 'bridge'
    side = intersections(road)
    df = pd.concat([df,side])
    df_road = df.loc[df.road==road,:].sort_values('km')
    df_road = df_road[['km','length','condition','lat','lon','intersection','model_type']].reset_index().drop('index',axis=1)
    
    df2 = pd.read_csv('_roads3.csv')
    df_start_end = df2.loc[df2.road==road,:]
    df_start_end = df_start_end.iloc[[0, -1]].reset_index().drop('index', axis=1)
    df_start_end = df_start_end.rename(columns={'chainage':'km'})
    df_start_end = df_start_end[['km','lat','lon']]
    df_start_end['id'] = 0
    df_start_end['model_type'] = 0
    df_start_end['length'] = 4
    df_start_end.loc[0,'id'] = 10000
    df_start_end.loc[0,'model_type'] = 'source'
    
    #make this so big that it will definetly end up at the end of the road, will be changed later
    df_start_end.loc[1,'id'] = 100000000
    df_start_end.loc[1,'model_type'] = 'sink'
    
    links = pd.DataFrame(columns=['km','length','condition','lat','lon','intersection'])
    
    for i in range(len(df_road)):
        links = links.append(df_road.iloc[i,:])
        if i == 0:
            links.loc[i,'km'] = df_road.loc[i,'km']
            links.loc[i,'lat'] = (df_road.loc[i,'lat'] + df_start_end.loc[0,'lat'])/2
            links.loc[i,'lon'] = (df_road.loc[i,'lon'] + df_start_end.loc[0,'lon'])/2
        elif i != 0:
            links.loc[i,'km'] = df_road.loc[i,'km'] - df_road.loc[i-1,'km']
            links.loc[i,'lat'] = (df_road.loc[i,'lat'] + df_road.loc[i-1,'lat'])/2
            links.loc[i,'lon'] = (df_road.loc[i,'lon'] + df_road.loc[i-1,'lon'])/2
        if i == len(df_road)-1 and len(df_road) > 1:
            links = links.append(df_start_end.iloc[1,:]).reset_index().drop('index',axis=1)
            links.loc[i+1,'km'] = df_start_end.loc[1,'km'] - df_road.loc[i-1,'km']
            links.loc[i+1,'lat'] = (df_road.loc[i,'lat'] + df_start_end.loc[1,'lat'])/2
            links.loc[i+1,'lon'] = (df_road.loc[i,'lon'] + df_start_end.loc[1,'lon'])/2
        if i == len(df_road)-1 and len(df_road) <= 1:
            links = links.append(df_start_end.iloc[1,:]).reset_index().drop('index',axis=1)
            links.loc[i+1,'km'] = df_start_end.loc[1,'km'] - df_road.loc[0,'km']
            links.loc[i+1,'lat'] = (df_road.loc[i,'lat'] + df_start_end.loc[1,'lat'])/2
            links.loc[i+1,'lon'] = (df_road.loc[i,'lon'] + df_start_end.loc[1,'lon'])/2
    
    links['id'] = (links.index * 2) + 10001
    links['length'] = links['km']*1000
    links['model_type'] = 'link'
    links['condition'] = 'NaN'
    links = links.drop('km',axis=1)
    df_road['id'] = (df_road.index * 2) + 10002
    df_road = pd.concat([df_road,links,df_start_end]).sort_values(['id']).reset_index().drop(['km','index'],axis=1)
    df_road.loc[len(df_road)-1,'id'] = 10000+len(df_road)-1
    df_road['road'] = road
    
    
    return df_road

df_road = model_structure('N1')
df_road.to_csv("./data/df_road.csv")

# main_road = intersections('N1')

# for i in main_road.intersection:
  #  print(i)
  #  a = model_structure(i)