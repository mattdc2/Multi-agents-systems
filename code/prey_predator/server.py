from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep

def wolf_sheep_portrayal(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Sheep:
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "grey",
                 "r": 0.5}

    elif type(agent) is Wolf:
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 2,
                 "Color": "red",
                 "r": 0.3}

    elif type(agent) is GrassPatch:
        portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 0,
                 "h": 0.9,
                 "w":0.9}
        if agent.grass_state == agent.countdown:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "white"

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    "grass_regrowth_time": UserSettableParameter("slider", "Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": UserSettableParameter("slider", "Initial Sheep Population", 100, 10, 300),
    "sheep_reproduce": UserSettableParameter("slider", "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01),
    "initial_wolves": UserSettableParameter("slider", "Initial Wolf Population", 50, 10, 300),
    "wolf_reproduce": UserSettableParameter("slider", "Wolf Reproduction Rate", 0.05, 0.01, 1.0, 0.01),
    "wolf_gain_from_food": UserSettableParameter("slider", "Wolf Gain From Food Rate", 20, 1, 50),
    "sheep_gain_from_food": UserSettableParameter("slider", "Sheep Gain From Food", 4, 1, 10),
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
