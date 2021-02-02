import sys

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from Vehicles import Truck

import pandas as pd


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
                self.space.place_agent(agent, (x, y))
                agent.pos = (x, y)

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")

    def step(self):

        if self.model.schedule.steps % 5 == 0:
            self.generate_truck()
        else:
            self.truck_generated_flag = False