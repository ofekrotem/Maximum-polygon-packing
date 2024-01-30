from .algo import Algo
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution


class GeneticAlgo (Algo):
    def __init__(self,shapes: list[Shape], cont: Container, pop_size: int, gens: int):
        super().__init__(shapes,cont)
        if pop_size<2:
            raise Exception("Population size must be at least 2")
        self.population_size = pop_size
        self.max_generations = gens
        self.curr_generation=[]
        self.next_generation=[]

    def run(self):
        self.curr_generation=self.generate_base_gen()
        for i in range(self.max_generations):
            print(f"Starting generation {i+1}")
            self.next_generation=self.generate_next_gen()
            self.curr_generation=self.next_generation

        sol = max(self.curr_generation,key=lambda s: s.grade())
        sol.visualize_solution()

    def generate_next_gen(self)->list[Solution]:
        # Generate new generation
        new_gen=[]
        max_sol=max(self.curr_generation,key=lambda s: s.grade())
        print(f"Best solution in prev generation: {max_sol.grade()}")
        new_gen.append(max_sol)
        for i in range(self.population_size - 1):
            # Select parents
            p1,p2=self.curr_generation[i],self.curr_generation[i+1]
            # Crossover
            child=self.crossover(p1,p2)
            # Add to new generation
            new_gen.append(child)
        return sorted(new_gen,key=lambda s: s.grade(),reverse=True)

    def generate_base_gen(self)->list[Solution]:
        lst=[]
        for i in range(self.population_size):
            lst.append(super().create_random_offset_solution("random"))
        return sorted(lst,key=lambda s: s.grade(),reverse=True)

    def crossover(self,s1:Solution,s2:Solution)->Solution:
        # Try to fit shapes that are in s2  and not in s1 into s1
        for i in range(len(s2.Items_ID)):
            if s2.Items_ID[i] not in s1.Items_ID:
                temps1=s1
                temps1.Items_ID.append(s2.Items_ID[i])
                temps1.X_Offset.append(s2.X_Offset[i])
                temps1.Y_Offset.append(s2.Y_Offset[i])
                if temps1.is_valid():
                    print("Merged shape into s1")
                    s1=temps1
        # Try to fit shapes that are in s1  and not in s2 into s2
        for i in range(len(s1.Items_ID)):
            if s1.Items_ID[i] not in s2.Items_ID:
                temps2=s2
                temps2.Items_ID.append(s1.Items_ID[i])
                temps2.X_Offset.append(s1.X_Offset[i])
                temps2.Y_Offset.append(s1.Y_Offset[i])
                if temps2.is_valid():
                    print("Merged shape into s2")
                    s2=temps2
        return max(s1,s2,key=lambda s: s.grade())
