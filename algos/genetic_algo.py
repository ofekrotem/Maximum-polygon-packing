import copy
import logging
import time
from tqdm import tqdm
from .algo import Algo, FindPositionClassification
from utils.Container import Container
from utils.Shape import Shape
from utils.Solution import Solution
import random
from concurrent.futures import ProcessPoolExecutor

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

    def run(self) -> Solution:
        start_time = time.time()
        self.curr_generation = self.generate_base_gen()
        end_time = time.time()
        duration = end_time - start_time
        max_sol = max(self.curr_generation, key=lambda s: s.grade())
        logging.info(f"Base generation completed in {duration:.3f} seconds\nBest solution with value: {max_sol.grade()}")
        best_grade_so_far = max_sol.grade()
        with tqdm(total=self.max_generations, desc=f"Running genetic algorithm - Best Grade in baseGen: {best_grade_so_far}", unit="gen") as pbar:
            for i in range(self.max_generations):
                logging.info(f"Starting generation {i + 1}")
                start_time = time.time()
                self.next_generation = self.generate_next_gen()
                end_time = time.time()
                duration = end_time - start_time
                self.curr_generation = self.next_generation
                max_sol = max(self.curr_generation, key=lambda s: s.grade())
                best_grade_so_far = max_sol.grade()
                logging.info(f"Generation {i + 1} completed in {duration:.3f} seconds\nBest solution with value: {best_grade_so_far}")
                print("len of shapes:", len(self.Shapes))
                if len(max_sol.Shapes) == len(self.Shapes):
                    logging.info(f"Found optimal solution in generation {i + 1}")
                    break
                pbar.set_description(f"Running genetic algorithm - Best Grade in gen {i+1}: {best_grade_so_far}")
                pbar.update(1)

        sol = max(self.curr_generation, key=lambda s: s.grade())
        logging.info(f"Best solution found: {sol}")
        return sol

    def generate_next_gen(self) -> list[Solution]:
        # Elitism: Keep the best solution
        # new_gen = [max(self.curr_generation, key=lambda s: s.grade())]
        futures = []
        # Generate new generation
        with ProcessPoolExecutor() as executor:
            for child in self.curr_generation:
                futures.append(executor.submit(self.mutate, child))

        new_gen = [future.result() for future in futures]

        return sorted(new_gen, key=lambda s: s.grade(), reverse=True)


    def generate_base_gen(self) -> list[Solution]:
        with ProcessPoolExecutor() as executor:
            futures = []

            for i in range(self.population_size):
                if i % 5 == 0:
                    futures.append(executor.submit(self.create_bottom_right_solution))
                elif i % 5 == 1:
                    futures.append(executor.submit(self.create_bottom_left_solution))
                elif i % 5 == 2:
                    futures.append(executor.submit(self.create_top_right_solution))
                elif i % 5 == 3:
                    futures.append(executor.submit(self.create_top_left_solution))
                else:
                    futures.append(executor.submit(self.create_random_offset_solution))

        solutions = [future.result() for future in futures]
        base_gen = sorted(solutions, key=lambda s: s.grade(), reverse=True)
        return base_gen

    def tournament_selection(self) -> Solution:
        # Tournament selection: Randomly select a subset of solutions and choose the best among them
        tournament_size = min(3, len(self.curr_generation))
        tournament_candidates = random.sample(self.curr_generation, tournament_size)
        winner = max(tournament_candidates, key=lambda s: s.grade())
        return winner

    def fit_remaining_shapes_in_solution(self, solution: Solution,classification: FindPositionClassification) -> Solution:
        solution_copy = copy.deepcopy(solution)
        solution_shape_ids = [shape.Index for shape in solution_copy.Shapes]
        remaining_shapes = [shape for shape in self.Shapes if shape.Index not in solution_shape_ids]
        remaining_shapes = self.sort_shapes_by_value(remaining_shapes)

        for shape in remaining_shapes:
            remaining_area = solution_copy.get_remaining_area_in_container()
            if shape.get_area() > remaining_area:
                logging.debug(f"Could not place shape {shape.Index}. Not enough space left.")
                continue
            if classification == FindPositionClassification.BOTTOM_LEFT:
                x, y = self.find_bottom_left_position(shape, solution_copy)
            elif classification == FindPositionClassification.TOP_LEFT:
                x, y = self.find_top_left_position(shape, solution_copy)
            elif classification == FindPositionClassification.BOTTOM_RIGHT:
                x, y = self.find_bottom_right_position(shape, solution_copy)
            elif classification == FindPositionClassification.TOP_RIGHT:
                x, y = self.find_top_right_position(shape, solution_copy)
            if x is not None and y is not None:
                logging.debug(f"Placed shape {shape.Index} with offset ({x}, {y}).")
            else:
                logging.debug(f"Could not place shape {shape.Index}. No valid position found.")

        return solution_copy

    def mutate(self, solution: Solution) -> Solution:
        print("Starting mutation")
        futures = []
        with ProcessPoolExecutor() as executor:
            futures.append(executor.submit(self.mutate_left_down, solution))
            futures.append(executor.submit(self.mutate_down_left, solution))
            futures.append(executor.submit(self.mutate_up_left, solution))
            futures.append(executor.submit(self.mutate_left_up, solution))
            futures.append(executor.submit(self.mutate_right_down, solution))
            futures.append(executor.submit(self.mutate_down_right, solution))
            futures.append(executor.submit(self.mutate_right_up, solution))
            futures.append(executor.submit(self.mutate_up_right, solution))



        solutions = [future.result() for future in futures]
        max_sol = max(solutions, key=lambda s: s.grade())
        print(f"Finished mutating - started with {len(solution.Shapes)} shapes, finished with {len(max_sol.Shapes)} shapes")

        return max_sol

    def mutate_left_down(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_left(solution)
        new_solution = self.push_shapes_down(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.BOTTOM_LEFT)
        return new_solution

    def mutate_down_left(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_down(solution)
        new_solution = self.push_shapes_left(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.BOTTOM_LEFT)
        return new_solution

    def mutate_up_left(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_up(solution)
        new_solution = self.push_shapes_left(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.TOP_LEFT)
        return new_solution

    def mutate_left_up(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_left(solution)
        new_solution = self.push_shapes_up(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.TOP_LEFT)
        return new_solution

    def mutate_right_down(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_right(solution)
        new_solution = self.push_shapes_down(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.BOTTOM_RIGHT)
        return new_solution

    def mutate_down_right(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_down(solution)
        new_solution = self.push_shapes_right(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.BOTTOM_RIGHT)
        return new_solution

    def mutate_right_up(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_right(solution)
        new_solution = self.push_shapes_up(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.TOP_RIGHT)
        return new_solution

    def mutate_up_right(self, solution: Solution) -> Solution:
        new_solution = self.push_shapes_up(solution)
        new_solution = self.push_shapes_right(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution,FindPositionClassification.TOP_RIGHT)
        return new_solution

    def push_shapes_left(self, solution: Solution) -> Solution:
        # Mutation: Push polygons left if possible while maintaining validity
        logging.debug(f"Pushing shapes left {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[0]))

        for shape in solution_shapes_sorted:
            left_limit = min(solution.Container.X_cor)
            right_limit = min(shape.get_real_coords()[0])
            while left_limit + 0.5 < right_limit - 0.5:
                sample_x = (left_limit + right_limit) // 2
                original_x_offset = shape.X_offset
                shape.X_offset += sample_x - right_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} left to {sample_x}")
                    right_limit = sample_x
                else:
                    shape.X_offset = original_x_offset
                    left_limit = sample_x
        return mutated_solution


    def push_shapes_down(self, solution: Solution) -> Solution:
        # Mutation: Push polygons down if possible while maintaining validity
        logging.debug(f"Pushing shapes down {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[1]))

        for shape in solution_shapes_sorted:
            bottom_limit = min(solution.Container.Y_cor)
            top_limit = min(shape.get_real_coords()[1])
            while bottom_limit + 0.5 < top_limit - 0.5:
                sample_y = (bottom_limit + top_limit) // 2
                original_y_offset = shape.Y_offset
                shape.Y_offset += sample_y - top_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} down to {sample_y}")
                    top_limit = sample_y
                else:
                    shape.Y_offset = original_y_offset
                    bottom_limit = sample_y

        return mutated_solution

    def push_shapes_up(self,solution: Solution) -> Solution:
        # Mutation: Push polygons up if possible while maintaining validity
        logging.debug(f"Pushing shapes up {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[1]), reverse=True)

        for shape in solution_shapes_sorted:
            top_limit = max(solution.Container.Y_cor)
            bottom_limit = max(shape.get_real_coords()[1])
            while bottom_limit + 0.5 < top_limit - 0.5:
                sample_y = (bottom_limit + top_limit) // 2
                original_y_offset = shape.Y_offset
                shape.Y_offset += sample_y - bottom_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} up to {sample_y}")
                    bottom_limit = sample_y
                else:
                    shape.Y_offset = original_y_offset
                    top_limit = sample_y

        return mutated_solution

    def push_shapes_right(self, solution: Solution) -> Solution:
        # Mutation: Push polygons right if possible while maintaining validity
        logging.debug(f"Pushing shapes right {solution}")
        mutated_solution = copy.deepcopy(solution)
        solution_shapes_sorted = sorted(mutated_solution.Shapes, key=lambda s: min(s.get_real_coords()[0]), reverse=True)

        for shape in solution_shapes_sorted:
            right_limit = max(solution.Container.X_cor)
            left_limit = max(shape.get_real_coords()[0])
            while left_limit + 0.5 < right_limit - 0.5:
                sample_x = (left_limit + right_limit) // 2
                original_x_offset = shape.X_offset
                shape.X_offset += sample_x - left_limit
                if mutated_solution.is_valid():
                    logging.debug(f"Mutated solution {solution} by moving shape {shape.Index} left to {sample_x}")
                    left_limit = sample_x
                else:
                    shape.X_offset = original_x_offset
                    right_limit = sample_x
        return mutated_solution
