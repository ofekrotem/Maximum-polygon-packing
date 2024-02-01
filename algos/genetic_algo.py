import copy
import json
from .algo import Algo, AlgoClassification
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution
from utils.utils import LoadJsonClassification, load_json_from_file
import random
random.seed(0)

class GeneticAlgo(Algo):
    def __init__(self, shapes: list[Shape], cont: Container, pop_size: int, gens: int, tries_on_random_creation: int,instance_name: str):
        super().__init__(shapes, cont, tries_on_random_creation)
        if pop_size < 2:
            raise Exception("Population size must be at least 2")
        self.population_size = pop_size
        self.max_generations = gens
        self.curr_generation = []
        self.next_generation = []
        self.instance_name = instance_name

    def run(self):
        self.curr_generation = self.generate_base_gen()
        for i in range(self.max_generations):
            print(f"Starting generation {i + 1}")
            self.next_generation = self.generate_next_gen()
            self.curr_generation = self.next_generation[:self.population_size // 2]  # Elitism: Keep the best half
            self.curr_generation.extend(self.next_generation[self.population_size // 2:])
            max_sol = max(self.curr_generation, key=lambda s: s.grade())
            print(f"Best solution in generation {i + 1}: {max_sol.grade()}")
        sol = max(self.curr_generation, key=lambda s: s.grade())
        sol.visualize_solution()

    def generate_next_gen(self) -> list[Solution]:
        # Elitism: Keep the best solution
        new_gen = [max(self.curr_generation, key=lambda s: s.grade())]
        # Generate new generation
        for i in range(self.population_size-1):
            # Select parents using tournament selection
            p1 = self.tournament_selection()
            p2 = self.tournament_selection()

            child = self.crossover(p1, p2)

            child = self.mutate(child)

            # Ensure diversity by checking if the child is significantly different from existing solutions
            if all(child.grade() != s.grade() for s in self.curr_generation):
                new_gen.append(child)
            else:
                # If not diverse, generate a new solution
                new_gen.append(self.create_random_offset_solution(AlgoClassification.SORT_BY_VALUE))

        return sorted(new_gen, key=lambda s: s.grade(), reverse=True)

    def generate_base_gen(self) -> list[Solution]:
        base_gen = load_json_from_file(f'./data/baseGens/{self.instance_name}_baseGen.json', LoadJsonClassification.BASE_GEN)
        if base_gen is None:
            lst = [self.create_random_offset_solution(AlgoClassification.SORT_BY_AREA) for _ in range(self.population_size)]
            base_gen = sorted(lst, key=lambda s: s.grade(), reverse=True)
            # save base_gen to file, base gen is a list of solutions
            solutions_as_dicts = [s.export_to_json() for s in base_gen]
            with open(f'./data/baseGens/{self.instance_name}_baseGen.json', 'w') as f:
                json.dump(solutions_as_dicts, f)
        else:
            # go over the list of solutions and assign the container and shapes list
            for s in base_gen:
                s.Container = self.Container
                s.Shapes = self.Shapes
        return base_gen

    def crossover(self, s1: Solution, s2: Solution) -> Solution:
        print("entered Crossover")
        s1_child = copy.deepcopy(s1)
        s2_child = copy.deepcopy(s2)

        # Try to fit shapes that are in s2 and not in s1 into s1
        for i in range(len(s2.Items_ID)):
            if s2.Items_ID[i] not in s1_child.Items_ID:
                temp_child = copy.deepcopy(s1_child)
                temp_child.Items_ID.append(s2.Items_ID[i])
                temp_child.X_Offset.append(s2.X_Offset[i])
                temp_child.Y_Offset.append(s2.Y_Offset[i])

                if temp_child.is_valid():
                    s1_child = copy.deepcopy(temp_child)
                    print(f"Merged shape into s1_child raising grade from {s1_child.grade()} to {temp_child.grade()}")

        # Try to fit shapes that are in s1 and not in s2 into s2
        for i in range(len(s1.Items_ID)):
            if s1.Items_ID[i] not in s2_child.Items_ID:
                temp_s2 = copy.deepcopy(s2_child)
                temp_s2.Items_ID.append(s1.Items_ID[i])
                temp_s2.X_Offset.append(s1.X_Offset[i])
                temp_s2.Y_Offset.append(s1.Y_Offset[i])

                if temp_s2.is_valid():
                    print(f"Merged shape into s2_child raising grade from {s2_child.grade()} to {temp_s2.grade()}")
                    s2_child = copy.deepcopy(temp_s2)

        return max(s1_child, s2_child, key=lambda s: s.grade())

    def tournament_selection(self) -> Solution:
        # Tournament selection: Randomly select a subset of solutions and choose the best among them
        tournament_size = min(3, len(self.curr_generation))
        tournament_candidates = random.sample(self.curr_generation, tournament_size)
        winner = max(tournament_candidates, key=lambda s: s.grade())
        return winner

    def mutate(self, solution: Solution) -> Solution:
    # Mutation: Randomly perturb the solution
        mutated_solution = copy.deepcopy(solution)  # Ensure not to modify the original solution

        for i in range(len(mutated_solution.Items_ID)):
            # Apply a small random perturbation to the offset
            mutated_solution.X_Offset[i] += random.uniform(-10, 10)
            mutated_solution.Y_Offset[i] += random.uniform(-10, 10)

            # Check if the mutated solution is valid
            if mutated_solution.is_valid():
                solution = copy.deepcopy(mutated_solution)
                print("Mutated solution")

        return solution

