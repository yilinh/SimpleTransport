import sys

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace

import pandas as pd



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
            #print(self.name + ' ' + str(self.length))
        except Exception as e:
            print("Oops!", e.__class__, "occurred in link.")

