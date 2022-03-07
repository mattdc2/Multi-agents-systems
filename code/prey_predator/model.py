"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
from random import randint

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """
    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheep:
        for _ in range(initial_sheep):
            pos = randint(0,self.height-1), randint(0,self.width-1)
            sheep_agent = Sheep(unique_id=self.next_id(), pos=pos, model=self, moore=True, energy=self.sheep_gain_from_food)
            self.schedule.add(sheep_agent)
            self.grid.place_agent(sheep_agent, pos)

        # Create wolves
        for _ in range(initial_wolves):
            pos = randint(0,self.height-1), randint(0,self.width-1)
            wolf_agent = Wolf(unique_id=self.next_id(), pos=pos, model=self, moore=True, energy=self.wolf_gain_from_food)
            self.schedule.add(wolf_agent)
            self.grid.place_agent(wolf_agent, pos)

        # Create grass patches
        for x in range(self.height):
            for y in range(self.width):
                pos = (x,y)
                grass_patch = GrassPatch(unique_id=self.next_id(), pos=pos, model=self, fully_grown=False)
                self.schedule.add(grass_patch)
                self.grid.place_agent(grass_patch, pos)     

    def create_sheep(self, pos):
        sheep = Sheep(unique_id=self.next_id(), pos=pos, model=self, moore=True, energy=self.sheep_gain_from_food)
        #add to the schedule
        self.schedule.add(sheep)
        self.grid.place_agent(Sheep, pos)  
                

    def create_wolf(self, pos):
        wolf = Wolf(unique_id=self.next_id(), pos=pos, model=self, moore=True, energy=self.wolf_gain_from_food)
        #add to the schedule
        self.schedule.add(wolf)
        self.grid.place_agent(wolf, pos)  
            

    def step(self):
        self.schedule.step()
        # Collect data
        self.datacollector.collect(self)
        # ... to be completed

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()
            #print(f"Number of wolves {self.datacollector.get_agent_vars_dataframe()['Wolves']}")
            #print(f"Number of sheep {self.datacollector.get_agent_vars_dataframe()['Sheep']}")


#model = WolfSheep()
#model.run_model()