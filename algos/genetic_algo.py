from algo import Algo
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution


class GeneticAlgo (Algo):
    def __init__(self,shapes: list[Shape], cont: Container, pop_size: int, gens: int, size:int):
        super().__init__(shapes,cont)
        self.population_size = pop_size
        self.max_generations = gens
        self.generation_size=size
        self.first_generation=[]

    def generate_first_gen(self)->list[Solution]:
        lst=[]
        for i in range(self.generation_size):
            lst.append(super().create_random_offset_solution("random"))
