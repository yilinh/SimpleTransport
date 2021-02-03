import sys

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace

import pandas as pd



class Truck(Agent):
    """A simple bridge agent"""
    #truck_flag = False
    go_to_next_flag = False

    def __init__(self, unique_id, model, location, location_offset=0, go_to_next_flag=False, next_location=0):
        super().__init__(unique_id, model)
        self.location = location
        self.next_location = next_location 
        self.location_offset = location_offset
        self.pos = location.pos
        self.name = ''
        self.length = 1
        