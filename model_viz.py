from mesa.visualization.ModularVisualization import ModularServer
from SimpleContinuousModule import SimpleCanvas
from model import BangladeshModel
from components import Infra, Source, Sink, Bridge, Link


def agent_portrayal(agent):

    portrayal = {
                 # "Shape": "rect",
                 "Shape": "circle",
                 "Filled": "true",
                 "Color": "Khaki",
                 "r": 2
                 # "w": max(agent.population / 100000 * 4, 4),
                 # "h": max(agent.population / 100000 * 4, 4)
                 }

    if isinstance(agent, Source):
        if agent.vehicle_generated_flag:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "red"
        portrayal["r"] = 5

    elif isinstance(agent, Sink):
        if agent.vehicle_removed_toggle:
            portrayal["Color"] = "LightSkyBlue"
        else:
            portrayal["Color"] = "LightPink"
        portrayal["r"] = 5

    elif isinstance(agent, Link):
        portrayal["Color"] = "Tan"
        portrayal["r"] = max(agent.vehicle_count * 4, 2)

    elif isinstance(agent, Bridge):
        portrayal["Color"] = "dodgerblue"
        portrayal["r"] = max(agent.vehicle_count * 4, 2)

    if isinstance(agent, Infra) and agent.name in ['Dhaka', 'Chittagong', "Cox's Bazar", 'Teknaf']:
        portrayal["Text"] = agent.name
        portrayal["Text_color"] = "DarkSlateGray"

    return portrayal


canvas_width = 400
canvas_height = 400

space = SimpleCanvas(agent_portrayal, canvas_width, canvas_height)

server = ModularServer(BangladeshModel,
                       [space],
                       "Simple Transport Model",
                       {})

server.port = 8521  # The default port
server.launch()
