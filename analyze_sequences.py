from collections import Counter, OrderedDict
import pandas as pd
import json
from tqdm import tqdm
import matplotlib.pyplot as plt

CROSS_SOLUTIONS_FILE = "first_cross_solutions.csv"
COUNT_FILE = "cross_ngram_count.json"


def count_tuples(solution: str, counter: Counter, k: int = 3) -> None:
    solution_seq = solution.split(" ")
    for i in range(len(solution_seq) - k + 1):
        subsequence = solution_seq[i:i+k]
        counter[" ".join(subsequence)] += 1
        

def count_all_tuples():
    counter = Counter()
    cross_solutions = pd.read_csv(CROSS_SOLUTIONS_FILE)
    for solution in tqdm(cross_solutions.solution):
        count_tuples(solution, counter)
    with open(COUNT_FILE, "w") as f:
        ordered_dict = OrderedDict(sorted(counter.items(), key=lambda t: -t[1]))
        json.dump(ordered_dict, f, indent=4)
    return counter

if __name__ == "__main__":
    counter = count_all_tuples()
    plt.bar(counter.keys, counter.values)

