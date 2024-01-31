import copy
from .algo import Algo, Classification
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution
import random
random.seed(0)

class GeneticAlgo(Algo):
    def __init__(self, shapes: list[Shape], cont: Container, pop_size: int, gens: int):
        super().__init__(shapes, cont)
        if pop_size < 2:
            raise Exception("Population size must be at least 2")
        self.population_size = pop_size
        self.max_generations = gens
        self.curr_generation = []
        self.next_generation = []
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8

    def run(self):
        self.curr_generation = self.generate_base_gen()
        for i in range(self.max_generations):
            print(f"Starting generation {i + 1}")
            self.adjust_parameters(i)
            self.next_generation = self.generate_next_gen()
            self.curr_generation = self.next_generation[:self.population_size // 2]  # Elitism: Keep the best half
            self.curr_generation.extend(self.next_generation[self.population_size // 2:])
            max_sol = max(self.curr_generation, key=lambda s: s.grade())
            print(f"Best solution in generation {i + 1}: {max_sol.grade()}")
        sol = max(self.curr_generation, key=lambda s: s.grade())
        sol.visualize_solution()

    def adjust_parameters(self, generation_number: int):
        # Adjust mutation and crossover rates dynamically
        max_gen = self.max_generations
        self.mutation_rate = max(0.1, 0.1 + 0.9 * (max_gen - generation_number) / max_gen)
        self.crossover_rate = min(0.8, 0.1 + 0.9 * (max_gen - generation_number) / max_gen)

    def generate_next_gen(self) -> list[Solution]:
        # Generate new generation
        new_gen = []
        for i in range(self.population_size):
            # Select parents using tournament selection
            p1 = self.tournament_selection()
            p2 = self.tournament_selection()

            # Crossover with a probability
            if random.random() < self.crossover_rate:
                child = self.crossover(p1, p2)
            else:
                child = p1  # No crossover, simply copy the parent

            # Mutation with a probability
            if random.random() < self.mutation_rate:
                child = self.mutate(child)

            # Ensure diversity by checking if the child is significantly different from existing solutions
            if all(child.grade() != s.grade() for s in self.curr_generation):
                new_gen.append(child)
            else:
                # If not diverse, generate a new solution
                new_gen.append(self.create_random_offset_solution(Classification.RANDOM))

        return sorted(new_gen, key=lambda s: s.grade(), reverse=True)

    def generate_base_gen(self) -> list[Solution]:
        lst = [self.create_random_offset_solution(Classification.RANDOM) for _ in range(self.population_size)]
        return sorted(lst, key=lambda s: s.grade(), reverse=True)

    def crossover(self, s1: Solution, s2: Solution) -> Solution:
        child = copy.deepcopy(s1)

        # Try to fit shapes that are in s2 and not in s1 into s1
        for i in range(len(s2.Items_ID)):
            if s2.Items_ID[i] not in child.Items_ID:
                temp_child = copy.deepcopy(child)
                temp_child.Items_ID.append(s2.Items_ID[i])
                temp_child.X_Offset.append(s2.X_Offset[i])
                temp_child.Y_Offset.append(s2.Y_Offset[i])

                if temp_child.is_valid():
                    child = temp_child
                    print("Merged shape into child")

        # Try to fit shapes that are in s1 and not in s2 into s2
        for i in range(len(child.Items_ID)):
            if child.Items_ID[i] not in s2.Items_ID:
                temp_s2 = copy.deepcopy(s2)
                temp_s2.Items_ID.append(child.Items_ID[i])
                temp_s2.X_Offset.append(child.X_Offset[i])
                temp_s2.Y_Offset.append(child.Y_Offset[i])

                if temp_s2.is_valid():
                    s2 = temp_s2
                    print("Merged shape into s2")

        return max(child, s2, key=lambda s: s.grade())

    def tournament_selection(self) -> Solution:
        # Tournament selection: Randomly select a subset of solutions and choose the best among them
        tournament_size = min(10, len(self.curr_generation))
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
                solution = mutated_solution
                print("Mutated solution")

        return solution

