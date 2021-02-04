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

def model_structure(road):
    df= pd.read_csv('./data/CandV_Bridges.csv')
    df_road = df.loc[df.road==road,:].sort_values('km')
    df_road = df_road[['km','length','condition','lat','lon']].reset_index().drop('index',axis=1)
    df_road['model_type'] = 'bridge'
    
    df2 = pd.read_csv('./data/_roads3.csv')
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
    
    links = pd.DataFrame(columns=['km','length','condition','lat','lon'])

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
        if i == len(df_road)-1:
            links = links.append(df_start_end.iloc[1,:]).reset_index().drop('index',axis=1)
            links.loc[i+1,'km'] = df_start_end.loc[1,'km'] - df_road.loc[i-1,'km']
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
df_road.to_csv("./data/df_road.csv)
