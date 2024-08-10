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
                all_grades_in_prev_gen = [sol.grade() for sol in self.curr_generation]
                if all(sol.grade() in all_grades_in_prev_gen for sol in self.next_generation):
                    logging.info(f"Generation {i + 1} is the same as previous generation. Exiting")
                    break
                self.curr_generation = self.next_generation
                max_sol = max(self.curr_generation, key=lambda s: s.grade())
                best_grade_so_far = max_sol.grade()
                logging.info(f"Generation {i + 1} completed in {duration:.3f} seconds\nBest solution with value: {best_grade_so_far}")
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


