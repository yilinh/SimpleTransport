import sys

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace

import pandas as pd


# ---------------------------------------------------------------

class Bridge(Agent):
    """A simple bridge agent"""
    toggle_flag = True

    def __init__(self, unique_id, model, LRP_m, length,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.name = name
        self.LRP_m = LRP_m  # in meters
        self.length = length  # in meters
        self.road_name = road_name

    def toggle(self):
        # dummy action
        self.toggle_flag = not self.toggle_flag
        if self.toggle_flag:
            self.length = self.length * 1.2
        else:
            self.length = self.length / 1.2

    def step(self):
        try:
            self.toggle()
            print(self.name + ' ' + str(self.length))
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")


# ---------------------------------------------------------------

class Link(Agent):
    """A simple bridge agent"""
    toggle_flag = True

    def __init__(self, unique_id, model, LRP_m, length,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.name = name
        self.LRP_m = LRP_m  # in meters
        self.length = length  # in meters
        self.road_name = road_name

    def toggle(self):
        # dummy action
        self.toggle_flag = not self.toggle_flag
        if self.toggle_flag:
            self.length = self.length * 1.2
        else:
            self.length = self.length / 1.2

    def step(self):
        try:
            self.toggle()
            print(self.name + ' ' + str(self.length))
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")


# ---------------------------------------------------------------

class Truck(Agent):
    """A simple bridge agent"""
    truck_flag = False

    def __init__(self, unique_id, model, location, location_offset=0):
        super().__init__(unique_id, model)
        self.location = location
        self.location_offset = location_offset
        self.pos = location.pos
        self.name = ''
        self.length = 1


# ---------------------------------------------------------------

class Source(Agent):
    """A simple bridge agent"""
    truck_generated_flag = False
    truck_counter = 0

    def __init__(self, unique_id, model, LRP_m, length,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.name = name
        self.LRP_m = LRP_m  # in meters
        self.length = length  # in meters
        self.road_name = road_name

    def generate_truck(self):
        try:

            agent = Truck('Truck' + str(self.truck_counter), self.model, self)

            if agent:
                self.model.schedule.add(agent)
                self.truck_counter += 1
                self.truck_generated_flag = True
                # self.space.place_agent(agent, (x, y))
                # agent.pos = (x, y)

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")

    def step(self):

        if self.model.schedule.steps % 5 == 0:
            self.generate_truck()
        else:
            truck_generated_flag = False


# ---------------------------------------------------------------

class Sink(Agent):
    """A simple bridge agent"""
    toggle_flag = True

    def __init__(self, unique_id, model, LRP_m, length,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.name = name
        self.LRP_m = LRP_m  # in meters
        self.length = length  # in meters
        self.road_name = road_name

    def toggle(self):
        # dummy action
        self.toggle_flag = not self.toggle_flag
        if self.toggle_flag:
            self.length = self.length * 1.2
        else:
            self.length = self.length / 1.2

    def step(self):
        try:
            self.toggle()
            print(self.name + ' ' + str(self.length))
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")


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

    def __init__(self, x_max=500, y_max=500, x_min=0, y_min=0):

        self.schedule = BaseScheduler(self)
        self.running = True

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

        df_bridges_all = []
        self.num_bridges = 0

        for road in roads:
            df_bridges_on_road = df[df['road'] == road].sort_values(by=['km'])

            if not df_bridges_on_road.empty:
                df_bridges_all.append(df_bridges_on_road)
                self.num_bridges += len(df_bridges_on_road.index)

        # self.num_agents = len(df.index)

        df = pd.concat(df_bridges_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        # def __init__(self, unique_id, model, LRP_m, LRP_name, length,
        #              condition, name='Unknown', road_name='Unknown')

        for df in df_bridges_all:
            for index, row in df.iterrows():

                model_type = row['model_type']

                agent = None

                if model_type == 'source':
                    agent = Source(index, self, row['km'] * 1000, row['length'],
                                   row['name'], row['road'])
                elif model_type == 'sink':
                    agent = Sink(index, self, row['km'] * 1000, row['length'],
                                 row['name'], row['road'])
                elif model_type == 'bridge':
                    agent = Bridge(index, self, row['km'] * 1000, row['length'],
                                   row['name'], row['road'])
                elif model_type == 'link':
                    agent = Link(index, self, row['km'] * 1000, row['length'] * 1000,
                                 row['name'], row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
