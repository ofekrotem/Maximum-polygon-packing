import argparse
import logging
from algos.genetic_algo import GeneticAlgo
from utils.utils import LoadJsonClassification, load_json_from_file

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Genetic Algorithm for Shape Placement')
    parser.add_argument('--pop_size', type=int, default=10, help='Population size')
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
    instance_data = load_json_from_file(args.instance, LoadJsonClassification.INSTANCE)
    logging.info(f"Loaded instance data from {args.instance}")

    # Initialize genetic algorithm with parameters
    algo = GeneticAlgo(pop_size=args.pop_size, gens=args.gens, tries_on_random_creation=args.tries, cont=instance_data[0], shapes=instance_data[1], instance_name= instance_data[0].Instance_Name)
    logging.info(f"Initialized Genetic Algorithm with pop_size={args.pop_size}, gens={args.gens}, tries_on_random_creation={args.tries}")

    # Run the algorithm
    algo.run()
    logging.info("Algorithm execution completed")

if __name__ == "__main__":
    main()
