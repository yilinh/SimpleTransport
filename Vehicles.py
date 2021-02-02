import sys

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace

import pandas as pd



class Truck(Agent):
    """A simple truck agent"""
    truck_flag = False

    def __init__(self, unique_id, model, lat, lon, location_offset=0):
        super().__init__(unique_id, model)
        self.lat = lat
        self.lon = lon
        self.location_offset = location_offset
        self.pos = (self.lat,self.lon)
        self.name = ''
        self.length = 1
