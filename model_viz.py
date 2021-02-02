from mesa.visualization.ModularVisualization import ModularServer

from SimpleContinuousModule import SimpleCanvas
from model import BangladeshModel
from model import Source
from model import Sink
from model import Link
from model import Truck


def agent_portrayal(agent):

    portrayal = {
                 # "Shape": "rect",
                 "Shape": "circle",
                 "Filled": "true",
                 "Color": "dodgerblue",
                 "r": max(agent.length, 1)
                 # "w": max(agent.population / 100000 * 4, 4),
                 # "h": max(agent.population / 100000 * 4, 4)
                 }

    # if type(agent) is Source:
    #     pass
    # elif agent.length > 50:
    #     portrayal["Color"] = "red"

    if type(agent) is Source:
        if agent.truck_generated_flag:
            portrayal["Color"] = "HotPink"
        else:
            portrayal["Color"] = "LightPink"
    elif type(agent) is Sink:
        portrayal["Color"] = "LightGray"
    elif type(agent) is Link:
        portrayal["Color"] = "Tan"
        portrayal["r"] = max(agent.length / 1000, 1)
    if type(agent) is Truck:
        portrayal['Color'] = "Red"

        
    # if agent.name in ['LRP008b', 'LRP012f']:
    #     portrayal["Text"] = agent.name
    #     portrayal["Text_color"] = "DarkGray"

    return portrayal


canvas_width = 500
canvas_height = 500

space = SimpleCanvas(agent_portrayal, canvas_width, canvas_height)

server = ModularServer(BangladeshModel,
                       [space],
                       "Bangladesh N1 Model",
                       {})

server.port = 8521  # The default
server.launch()
