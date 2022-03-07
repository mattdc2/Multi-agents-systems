from mesa import Agent
from prey_predator.random_walk import RandomWalker
import random as rd

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """
    energy = None

    def __init__(self, unique_id, pos, model, moore=True, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.pos = pos
        self.model = model

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.eat_grass()
        self.reproduce()
        self.decrease_energy()
        if self.energy == 0:
            self.die()
    
    def eat_grass(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if type(cellmate) is GrassPatch: 
                if cellmate.fully_grown : 
                    self.energy += self.model.sheep_gain_from_food
                    cellmate.get_eaten_by_sheep()    
                break

    def decrease_energy(self):
        self.energy -=1

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
 
    def reproduce(self):
        if rd.random()<self.model.sheep_reproduce:
            new_sheep = Sheep(self.model.next_id(), self.pos, self.model, self.moore, 2*self.model.sheep_gain_from_food)
            self.model.schedule.add(new_sheep)
            self.model.grid.place_agent(new_sheep, self.pos)

class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.pos = pos
        self.model = model

    def step(self):
        self.random_move()
        self.eat_sheep()
        self.reproduce()
        self.decrease_energy()
        if self.energy == 0 :
            self.die()
    
    def eat_sheep(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if type(cellmate) is Sheep: #à tester. voir comment reconnaître les moutons     
                self.energy += self.model.sheep_gain_from_food
                cellmate.die()
            break

    def reproduce(self):
        if rd.random()<self.model.sheep_reproduce:
            new_wolf = Wolf(self.model.next_id(), self.pos, self.model, self.moore, 2*self.model.wolf_gain_from_food)
            self.model.schedule.add(new_wolf)
            self.model.grid.place_agent(new_wolf, self.pos)

    def decrease_energy(self):
        self.energy -=1

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """
    def __init__(self, unique_id, pos, model, fully_grown = True, countdown = 10):
        """
        Creates a new patch of grass
        Args:
            fully_grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.grass_state = countdown  # variable d'état donnant le nombre de jours restant avant que l'herbe ne pousse

    def step(self):
        self.grow()
        self.get_eaten_by_sheep()
    
    def grow(self):
        if not self.fully_grown :
            self.grass_state -= 1
            if self.grass_state == 0 :
                self.fully_grown = True
                self.grass_state = self.countdown
    
    def get_eaten_by_sheep(self):
        self.fully_grown=False  
        self.grass_state = self.countdown



