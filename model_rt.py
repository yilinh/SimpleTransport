
from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, Bridge, Link
import pandas as pd
import matplotlib.pyplot as plt

import networkx as nx 

# ---------------------------------------------------------------
# input: latitude and Longitude in Decimal Degrees (DD)
def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    # add edges (margins) to the bounding box
    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio
    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# 1 tick 1 min
class BangladeshModel(Model):
    """class variable"""
    step_time = 1  # 1 step is 1 min

    """local"""
    infra_dict = {}

    def __init__(self, x_max=500, y_max=500, x_min=0, y_min=0):


        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids = None
        self. G = nx.Graph()
        
        df = pd.read_csv('./data/simpleTransport.csv')

        roads = [
            'N1',
            'N2',
            'N3',
            'N4',
            'N5',
            'N6',
            'N7',
            'N8'
        ]

        df_objects_all = []
        self.num_bridges = 0

        for road in roads:
            df_objects_on_road = df[df['road'] == road].sort_values(by=['id'])

            if not df_objects_on_road.empty:
                df_objects_all.append(df_objects_on_road)
                self.path_ids = df_objects_on_road['id']

                # self.num_agents = len(df.index)

        df = pd.concat(df_objects_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)
        #create an undirected graph 
        

        for df in df_objects_all:
            for index, row in df.iterrows():

                model_type = row['model_type']
                agent = None

                if model_type == 'source':
                    agent = Source(row['id'], self, row['length'], row['name'], row['road'])
                elif model_type == 'sink':
                    agent = Sink(row['id'], self, row['length'], row['name'], row['road'])
                elif model_type == 'bridge':
                    agent = Bridge(row['id'], self, row['length'], row['name'], row['road'])
                    self.num_bridges += 1
                elif model_type == 'link':
                    agent = Link(row['id'], self, row['length'], row['name'], row['road'])

                if agent:
                    self.schedule.add(agent)
                    #self.infra_dict[agent.unique_id]=agent
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)
        
        self.graph_positions={}                                          # creating a dictionary to store positions in networkx graph
        for agent in list(self.schedule.agents):
            if type(agent) is 'Source' or 'Bridge' or 'Link':
                self.G.add_node(agent.unique_id, label=agent)            #add a node in graph with the agent
                self.graph_positions[agent.unique_id] = agent.pos        #primarily for visualization purposes
        
        
        node_list= list(self.G.nodes)                                 
        for i in range(len(node_list)):
            if i < len(node_list)-1:                                       #except for the last node
                self.G.add_edge(node_list[i],node_list[i+1])

    def step(self):
        """Advance the model by one step."""
        #nx.draw(self.G, pos=self.graph_positions, with_labels=True)
        #plt.show()
        self.schedule.step()


# ---------------------------------------------------------------
# run model for 100 steps

sim_model = BangladeshModel()
for i in range(30):
    sim_model.step()


