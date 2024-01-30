from Soultion import Solution
import logging

# TODO need to add here a method

"""
This function adds two numbers

:param a: container (convex region in the plane).
:param b: collection of "shape" in a list.
:return: solution instance
"""

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


class GreedyAlgorithm:
    @staticmethod
    def solve(container, shapes, max_iterations=10):
        logging.info("Starting GreedyAlgorithm solve method")

        # Sort shapes in descending order of rate using a lambda function
        shapes = sorted(shapes, key=lambda shape: shape.get_rate(), reverse=True)

        # Initialize the solution object
        solution = Solution(container.Instance_Name, 0, "", [], [], [], [])

        # Track the number of iterations
        iteration_count = 0

        for shape in shapes:
            logging.info(f"Iteration {iteration_count + 1}")

            max_offset_value = 0
            max_x_offset = 0
            max_y_offset = 0

            # Iterate through container X and Y coordinates to find a suitable offset
            for i in range(len(container.X_cor)):
                x = container.X_cor[i]
                y = container.Y_cor[i]

                # Check if the shape can fit at the current offset
                if all(x + dx in container.X_cor and y + dy in container.Y_cor for dx, dy in
                       zip(shape.X_cor, shape.Y_cor)):
                    offset_value = shape.Value * shape.Quantity

                    # Update the maximum offset value and coordinates if a better offset is found
                    if offset_value > max_offset_value:
                        max_offset_value = offset_value
                        max_x_offset = x
                        max_y_offset = y

            # Add the shape to the solution if a valid offset was found
            if max_offset_value > 0:
                solution.Items_Num += shape.Quantity
                solution.Items_ID.append(shape.Index)
                solution.X_Offset.append(max_x_offset)
                solution.Y_Offset.append(max_y_offset)

            # Increment the iteration count
            iteration_count += 1

            # Check if the maximum number of iterations is reached
            if iteration_count >= max_iterations:
                logging.info("Maximum iterations reached. Exiting loop.")
                break

        # Calculate the total value of the solution
        solution.Meta = f"Total value: {sum(shape.Value for shape in solution)}"

        logging.info("GreedyAlgorithm solve method completed successfully.")


        # return solution
