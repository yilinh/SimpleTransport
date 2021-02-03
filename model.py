
from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, Bridge, Link
import pandas as pd


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
    # infra_dict = {}

    def __init__(self, x_max=500, y_max=500, x_min=0, y_min=0):

        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids = None

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
                    # self.infra_dict[agent.unique_id] = agent
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


# ---------------------------------------------------------------
# run model for 100 steps
# sim_model = BangladeshModel()
# for i in range(200):
#     sim_model.step()
