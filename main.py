import argparse
import logging
import os
from algos.genetic_algo import GeneticAlgo
from utils.utils import load_json_from_file
import time

def setup_logging():
    log_file = 'logs.txt'
    if os.path.exists(log_file):
        os.remove(log_file)
    logging.basicConfig(filename="logs.txt",level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Genetic Algorithm for Shape Placement')
    parser.add_argument('--pop_size', type=int, default=4, help='Population size')
    parser.add_argument('--gens', type=int, default=10, help='Number of generations')
    parser.add_argument('--tries', type=int, default=10, help='Tries on random creation')
    parser.add_argument('--instance', type=str, required=True, help='Path to instance JSON file')
    return parser.parse_args()

def main():
    # Setup logging
    setup_logging()

    # Parse command-line arguments
    args = parse_arguments()

    # Load instance data
    instance_data = load_json_from_file(args.instance)
    logging.info(f"Loaded instance data from {args.instance}")

    # Initialize genetic algorithm with parameters
    algo = GeneticAlgo(pop_size=args.pop_size, gens=args.gens, tries_on_random_creation=args.tries, cont=instance_data[0], shapes=instance_data[1], instance_name= instance_data[0].Instance_Name)
    logging.info(f"Initialized Genetic Algorithm with pop_size={args.pop_size}, gens={args.gens}, tries_on_random_creation={args.tries}")

    # Run the algorithm
    start_time = time.time()
    solution = algo.run()
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Algorithm execution completed\nTotal time taken: {duration:.3f} seconds")
    solution.visualize_solution()

if __name__ == "__main__":
    main()
