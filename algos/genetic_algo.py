import copy
import logging
import time
from tqdm import tqdm
from .algo import Algo
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution
import random

random.seed(0)

class GeneticAlgo(Algo):
    def __init__(self, shapes: list[Shape], cont: Container, pop_size: int, gens: int, tries_on_random_creation: int, instance_name: str):
        super().__init__(shapes, cont, tries_on_random_creation)
        if pop_size < 2:
            raise Exception("Population size must be at least 2")
        self.population_size = pop_size
        self.max_generations = gens
        self.curr_generation = []
        self.next_generation = []
        self.instance_name = instance_name

    def run(self):
        start_time = time.time()

        self.curr_generation = self.generate_base_gen()
        max_sol = max(self.curr_generation, key=lambda s: s.grade())
        logging.info(f"Best solution in base generation: {max_sol.grade()}")
        best_grade_so_far = max_sol.grade()
        with tqdm(total=self.max_generations, desc=f"Running genetic algorithm - Best Grade in baseGen: {best_grade_so_far}", unit="gen") as pbar:
            for i in range(self.max_generations):
                logging.info(f"Starting generation {i + 1}")
                self.next_generation = self.generate_next_gen()
                self.curr_generation = self.next_generation
                max_sol = max(self.curr_generation, key=lambda s: s.grade())
                logging.info(f"Best solution in generation {i+1}: {max_sol.grade()}")
                best_grade_so_far = max_sol.grade()
                pbar.set_description(f"Running genetic algorithm - Best Grade in gen {i+1}: {best_grade_so_far}")
                pbar.update(1)

        sol = max(self.curr_generation, key=lambda s: s.grade())
        logging.info(f"Best solution found: {sol}")
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Total time taken: {duration:.3f} seconds")
        sol.visualize_solution()

    def generate_next_gen(self) -> list[Solution]:
        # Elitism: Keep the best solution
        # new_gen = [max(self.curr_generation, key=lambda s: s.grade())]
        new_gen = []
        # Generate new generation
        for child in self.curr_generation:
            child = self.mutate(child)
            new_gen.append(child)

        return sorted(new_gen, key=lambda s: s.grade(), reverse=True)


    def generate_base_gen(self) -> list[Solution]:
        lst = []
        for i in range(self.population_size):
            if i % 2 == 0:
                solution = self.create_random_offset_solution()
            else:
                solution = self.create_bottom_left_solution()
            lst.append(solution)

        base_gen = sorted(lst, key=lambda s: s.grade(), reverse=True)
        return base_gen

    def crossover(self, s1: Solution, s2: Solution) -> Solution:
        logging.debug("entered Crossover")
        s1_child = copy.deepcopy(s1)
        s2_child = copy.deepcopy(s2)

        # Try to fit shapes that are in s2 and not in s1 into s1
        for shape in s2_child.Shapes:
            if shape not in s1_child.Shapes:
                temp_child = copy.deepcopy(s1_child)
                temp_child.Shapes.append(shape)

                if temp_child.is_valid():
                    s1_child = copy.deepcopy(temp_child)
                    logging.info(f"Merged shape into s1_child raising grade from {s1_child.grade()} to {temp_child.grade()}")

        # Try to fit shapes that are in s1 and not in s2 into s2
        for shape in s1_child.Shapes:
            if shape not in s2_child.Shapes:
                temp_s2 = copy.deepcopy(s2_child)
                temp_s2.Shapes.append(shape)

                if temp_s2.is_valid():
                    logging.info(f"Merged shape into s2_child raising grade from {s2_child.grade()} to {temp_s2.grade()}")
                    s2_child = copy.deepcopy(temp_s2)

        return max(s1_child, s2_child, key=lambda s: s.grade())

    def tournament_selection(self) -> Solution:
        # Tournament selection: Randomly select a subset of solutions and choose the best among them
        tournament_size = min(3, len(self.curr_generation))
        tournament_candidates = random.sample(self.curr_generation, tournament_size)
        winner = max(tournament_candidates, key=lambda s: s.grade())
        return winner

    def fit_remaining_shapes_in_solution(self, solution: Solution) -> Solution:
        solution_copy = copy.deepcopy(solution)
        remaining_shapes = [shape for shape in self.Shapes if shape not in solution_copy.Shapes]
        remaining_shapes = self.sort_shapes_random_algo_classification(remaining_shapes)

        for shape in remaining_shapes:
            remaining_area = solution_copy.get_remaining_area_in_container()
            if shape.get_area() > remaining_area:
                print(f"Could not place shape {shape.Index}. Not enough space left.")
                continue
            x,y = self.find_bottom_left_position(shape, solution_copy)
            if x is not None and y is not None:
                print(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                print(f"Could not place shape {shape.Index}. No valid position found.")

        return solution_copy

    def mutate(self, solution: Solution) -> Solution:
        solution1 = self.push_shapes_left(solution)
        solution1 = self.push_shapes_down(solution)
        solution1 = self.fit_remaining_shapes_in_solution(solution1)

        solution2 = self.push_shapes_down(solution)
        solution2 = self.push_shapes_left(solution)
        solution2 = self.fit_remaining_shapes_in_solution(solution2)

        solution = max(solution1, solution2, key=lambda s: s.grade())

        return solution

    def push_shapes_left(self, solution: Solution) -> Solution:
        # Mutation: Push polygons left if possible while maintaining validity
        logging.info(f"Mutating solution {solution}")
        print("starting mutation")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[0]))

        for shape in solution_shapes_sorted:
            print(f"Shape {shape.Index}")
            left_limit = min(solution.Container.X_cor)
            right_limit = min(shape.get_real_coords()[0])
            while left_limit + 0.5 < right_limit - 0.5:
                print(f"Left: {left_limit}, Right: {right_limit}")
                sample_x = (left_limit + right_limit) // 2
                original_x_offset = shape.X_offset
                shape.X_offset += sample_x - right_limit
                if mutated_solution.is_valid():
                    print(f"Valid solution found at {sample_x}")
                    logging.info(f"Mutated solution {solution} by moving shape {shape.Index} to {sample_x}")
                    right_limit = sample_x
                else:
                    print(f"Invalid solution found at {sample_x}")
                    shape.X_offset = original_x_offset
                    left_limit = sample_x
        return mutated_solution


    def push_shapes_down(self, solution: Solution) -> Solution:
        # Mutation: Push polygons down if possible while maintaining validity
        logging.info(f"Mutating solution {solution}")
        print("starting mutation")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[1]))

        for shape in solution_shapes_sorted:
            print(f"Shape {shape.Index}")
            left_limit = min(solution.Container.Y_cor)
            right_limit = min(shape.get_real_coords()[1])
            while left_limit + 0.5 < right_limit - 0.5:
                print(f"Left: {left_limit}, Right: {right_limit}")
                sample_y = (left_limit + right_limit) // 2
                original_y_offset = shape.Y_offset
                shape.Y_offset += sample_y - right_limit
                if mutated_solution.is_valid():
                    print(f"Valid solution found at {sample_y}")
                    logging.info(f"Mutated solution {solution} by moving shape {shape.Index} to {sample_y}")
                    right_limit = sample_y
                else:
                    print(f"Invalid solution found at {sample_y}")
                    shape.Y_offset = original_y_offset
                    left_limit = sample_y

        return mutated_solution
