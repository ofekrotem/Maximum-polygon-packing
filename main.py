from algos.genetic_algo import GeneticAlgo
from utils.utils import load_json_from_file

if __name__ == "__main__":
    cont, shapes = load_json_from_file('./data/atris42.cgshop2024_instance.json')
    algo = GeneticAlgo(shapes, cont, 10, 10)
    algo.run()
