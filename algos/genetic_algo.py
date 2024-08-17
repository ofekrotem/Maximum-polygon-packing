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
    """
    A class representing a genetic algorithm for solving the max packing polygons problem.

    Attributes:
        population_size (int): Size of the population in each generation.
        max_generations (int): Maximum number of generations to run the algorithm.
        curr_generation (list[Solution]): Current generation of solutions.
        next_generation (list[Solution]): Next generation of solutions.
        instance_name (str): Name of the instance for logging purposes.
    """

    def __init__(self, shapes: list[Shape], cont: Container, pop_size: int, gens: int, tries_on_random_creation: int, instance_name: str):
        """
        Initializes the GeneticAlgo class with shapes, container, population size, number of generations, and instance name.

        Args:
            shapes (list[Shape]): List of shapes to be packed.
            cont (Container): The container in which the shapes should be packed.
            pop_size (int): The size of the population.
            gens (int): The number of generations to run.
            tries_on_random_creation (int): Number of tries allowed for random solution creation.
            instance_name (str): The name of the instance for logging.
        """
        super().__init__(shapes, cont, tries_on_random_creation, instance_name)
        if pop_size < 2:
            raise Exception("Population size must be at least 2")
        self.population_size = pop_size
        self.max_generations = gens
        self.curr_generation = []
        self.next_generation = []

    def run(self) -> Solution:
        """
        Runs the genetic algorithm, generating solutions over multiple generations.

        Returns:
            Solution: The best solution found after running the algorithm.
        """
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
                if len(max_sol.Shapes) == len(self.Shapes):
                    logging.info(f"Found optimal solution in generation {i + 1}")
                    break
                pbar.set_description(f"Running genetic algorithm - Best Grade in gen {i+1}: {best_grade_so_far}")
                pbar.update(1)

        sol = max(self.curr_generation, key=lambda s: s.grade())
        logging.info(f"Best solution found: {sol}")
        return sol

    def generate_next_gen(self) -> list[Solution]:
        """
        Generates the next generation of solutions by mutating and crossing over the current generation.

        Returns:
            list[Solution]: The new generation of solutions.
        """
        futures = []
        with ProcessPoolExecutor() as executor:
            for child in self.curr_generation:
                futures.append(executor.submit(self.mutate, child))

        new_gen = [future.result() for future in futures]
        max_sol = max(new_gen, key=lambda s: s.grade())
        futures = []
        with ProcessPoolExecutor() as executor:
            for index1, parent1 in enumerate(new_gen):
                for index2, parent2 in enumerate(new_gen):
                    if index1 < index2:
                        futures.append(executor.submit(self.crossover, parent1, parent2))
        new_gen = [future.result() for future in futures]
        new_gen.append(max_sol)
        new_gen = sorted(new_gen, key=lambda s: s.grade(), reverse=True)
        return new_gen[:self.population_size]

    def generate_base_gen(self) -> list[Solution]:
        """
        Generates the initial base generation of solutions.

        Returns:
            list[Solution]: The base generation of solutions.
        """
        shapes_sorted_by_real_value = self.sort_shapes_by_real_value(self.Shapes)
        with ProcessPoolExecutor() as executor:
            futures = []
            for i in range(self.population_size):
                if i % 5 == 0:
                    futures.append(executor.submit(self.create_bottom_right_solution, shapes_sorted_by_real_value))
                elif i % 5 == 1:
                    futures.append(executor.submit(self.create_bottom_left_solution, shapes_sorted_by_real_value))
                elif i % 5 == 2:
                    futures.append(executor.submit(self.create_top_right_solution, shapes_sorted_by_real_value))
                elif i % 5 == 3:
                    futures.append(executor.submit(self.create_top_left_solution, shapes_sorted_by_real_value))
                else:
                    futures.append(executor.submit(self.create_random_offset_solution, shapes_sorted_by_real_value))

        solutions = [future.result() for future in futures]
        base_gen = sorted(solutions, key=lambda s: s.grade(), reverse=True)
        return base_gen

    def mutate(self, solution: Solution) -> Solution:
        """
        Applies multiple mutation strategies to a solution.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution with the best grade.
        """
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

        return max_sol

    def mutate_left_down(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes to the left and then down.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_left(solution)
        new_solution = self.push_shapes_down(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.BOTTOM_LEFT)
        return new_solution

    def mutate_down_left(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes down and then to the left.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_down(solution)
        new_solution = self.push_shapes_left(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.BOTTOM_LEFT)
        return new_solution

    def mutate_up_left(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes up and then to the left.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_up(solution)
        new_solution = self.push_shapes_left(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.TOP_LEFT)
        return new_solution

    def mutate_left_up(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes to the left and then up.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_left(solution)
        new_solution = self.push_shapes_up(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.TOP_LEFT)
        return new_solution

    def mutate_right_down(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes to the right and then down.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_right(solution)
        new_solution = self.push_shapes_down(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.BOTTOM_RIGHT)
        return new_solution

    def mutate_down_right(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes down and then to the right.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_down(solution)
        new_solution = self.push_shapes_right(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.BOTTOM_RIGHT)
        return new_solution

    def mutate_right_up(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes to the right and then up.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_right(solution)
        new_solution = self.push_shapes_up(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.TOP_RIGHT)
        return new_solution

    def mutate_up_right(self, solution: Solution) -> Solution:
        """
        Mutates a solution by pushing shapes up and then to the right.

        Args:
            solution (Solution): The solution to mutate.

        Returns:
            Solution: The mutated solution.
        """
        new_solution = self.push_shapes_up(solution)
        new_solution = self.push_shapes_right(new_solution)
        new_solution = self.fit_remaining_shapes_in_solution(new_solution, FindPositionClassification.TOP_RIGHT)
        return new_solution

    def crossover(self, parent1: Solution, parent2: Solution) -> Solution:
        """
        Performs crossover between two parent solutions to create a new solution.

        Args:
            parent1 (Solution): The first parent solution.
            parent2 (Solution): The second parent solution.

        Returns:
            Solution: The resulting solution from the crossover.
        """
        shapes_set = set(parent1.Shapes)
        for shape in parent2.Shapes:
            if shape.Index not in [s.Index for s in shapes_set]:
                shapes_set.add(shape)
        shapes_sorted_by_calculated_value = self.sort_shapes_by_value(list(shapes_set))
        futures = []
        with ProcessPoolExecutor() as executor:
            futures.append(executor.submit(self.create_bottom_left_solution, list(shapes_sorted_by_calculated_value)))
            futures.append(executor.submit(self.create_bottom_right_solution, list(shapes_sorted_by_calculated_value)))
            futures.append(executor.submit(self.create_top_left_solution, list(shapes_sorted_by_calculated_value)))
            futures.append(executor.submit(self.create_top_right_solution, list(shapes_sorted_by_calculated_value)))

        solutions = [future.result() for future in futures]
        max_sol = max(solutions, key=lambda s: s.grade())
        return max_sol
