import random
from copy import deepcopy
from Soultion import Solution


def _roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]

    selected = random.choices(population, weights=probabilities)[0]
    return selected


class GeneticAlgorithm:
    def __init__(self, container, shapes, population_size=100, num_generations=100, mutation_rate=0.01):
        self.container = container
        self.shapes = shapes
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate

    def solve(self):
        population = self._create_initial_population()
        best_solution = None

        for generation in range(self.num_generations):
            fitness_scores = [self._calculate_fitness(solution) for solution in population]
            sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
            current_best_solution = sorted_population[0]

            if best_solution is None or self._calculate_fitness(best_solution) < self._calculate_fitness(
                    current_best_solution):
                best_solution = deepcopy(current_best_solution)

            new_population = [current_best_solution]  # Elitism

            while len(new_population) < self.population_size:
                parent1 = _roulette_wheel_selection(population, fitness_scores)
                parent2 = _roulette_wheel_selection(population, fitness_scores)
                offspring = self._crossover(parent1, parent2)
                offspring = self._mutate(offspring)
                new_population.append(offspring)

            population = new_population

        return best_solution

    def _create_initial_population(self):
        population = []
        for _ in range(self.population_size):
            solution = Solution("genetic", self.container.Instance_Name, 0, "", [], [], [])
            available_shapes = deepcopy(self.shapes)

            while len(available_shapes) > 0:
                shape = random.choice(available_shapes)
                x_offset, y_offset = self._get_valid_offset(shape)

                if x_offset is None or y_offset is None:
                    break

                solution.Items_Num += shape.Quantity
                solution.Items_ID.append(shape.Index)
                solution.X_Offset.append(x_offset)
                solution.Y_Offset.append(y_offset)

                available_shapes.remove(shape)

            population.append(solution)

        return population

    def _calculate_fitness(self, solution):
        total_value = sum(shape.Value for shape in solution)
        return total_value

    def _crossover(self, parent1, parent2):
        child = Solution("genetic", self.container.Instance_Name, 0, "", [], [], [])
        available_shapes = deepcopy(self.shapes)

        for i in range(len(parent1.Items_ID)):
            if random.random() < 0.5:
                shape = parent1.Items_ID[i]
                x_offset = parent1.X_Offset[i]
                y_offset = parent1.Y_Offset[i]
            else:
                shape = parent2.Items_ID[i]
                x_offset = parent2.X_Offset[i]
                y_offset = parent2.Y_Offset[i]

            if not self._is_overlap(child, x_offset, y_offset):
                child.Items_Num += self.shapes[shape].Quantity
                child.Items_ID.append(shape)
                child.X_Offset.append(x_offset)
                child.Y_Offset.append(y_offset)

            if shape in available_shapes:
                available_shapes.remove(shape)

        for shape in available_shapes:
            x_offset, y_offset = self._get_valid_offset(self.shapes[shape])

            if x_offset is not None and y_offset is not None:
                child.Items_Num += self.shapes[shape].Quantity
                child.Items_ID.append(shape)
                child.X_Offset.append(x_offset)
                child.Y_Offset.append(y_offset)

        return child

    def _mutate(self, solution):
        for i in range(len(solution.Items_ID)):
            if random.random() < self.mutation_rate:
                shape = solution.Items_ID[i]
                x_offset, y_offset = self._get_valid_offset(self.shapes[shape])

                if x_offset is not None and y_offset is not None:
                    solution.X_Offset[i] = x_offset
                    solution.Y_Offset[i] = y_offset

        return solution

    def _is_overlap(self, solution, x_offset, y_offset):
        for i in range(len(solution.Items_ID)):
            existing_shape = solution.Items_ID[i]
            existing_x = solution.X_Offset[i]
            existing_y = solution.Y_Offset[i]

            if self._is_colliding(self.shapes[existing_shape], existing_x, existing_y, x_offset,
                                  y_offset):
                return True

        return False

    def _is_colliding(self, shape1, x1, y1, x2, y2):
        for dx, dy in zip(shape1.X_cor, shape1.Y_cor):
            if x1 + dx in self.container.X_cor and y1 + dy in self.container.Y_cor:
                if x2 + dx in self.container.X_cor and y2 + dy in self.container.Y_cor:
                    return True

        return False

    def _get_valid_offset(self, shape):
        for i in range(len(self.container.X_cor)):
            x = self.container.X_cor[i]
            y = self.container.Y_cor[i]

            if all(x + dx in self.container.X_cor and y + dy in self.container.Y_cor for dx, dy in
                   zip(shape.X_cor, shape.Y_cor)):
                return x, y

        return None, None

    '''
algorithm = GeneticAlgorithm(container, shapes)
best_solution = algorithm.solve()
    '''
