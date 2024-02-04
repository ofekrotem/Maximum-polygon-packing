from algos.genetic_algo import GeneticAlgo
from utils.utils import LoadJsonClassification, load_json_from_file

if __name__ == "__main__":
    cont, shapes = load_json_from_file('./data/atris42.cgshop2024_instance.json', LoadJsonClassification.INSTANCE)
    algo = GeneticAlgo(shapes=shapes, cont=cont, pop_size=10,gens=10,tries_on_random_creation=1000, instance_name=cont.Instance_Name)
    algo.run()
