from algos.algo import Algo
from utils.utils import load_json_from_file

if __name__ == "__main__":
    cont, shapes = load_json_from_file('./data/atris42.cgshop2024_instance.json')
    algo = Algo(shapes, cont)
    lst=[]
    for i in range(9):
        lst.append(algo.create_random_offset_solution("random"))
    max(lst, key= lambda s : s.grade()).visualize_solution()
