import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
from tqdm import tqdm
import pandas as pd


def extract_solution(url: str) -> List[Tuple[str, str]]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results: List[BeautifulSoup] = soup.find_all("div", {"class": "algorithm well"})

    # scramble_div = results[0]
    solution_div = results[1]
    elements: List[BeautifulSoup] = solution_div.find_all("br")
    solution = []
    for br in elements[:-1]:
        moves = br.next_sibling
        if (moves):
            next_ = moves.next_sibling.text.split("\n")
            step = next_[2].strip() if len(next_) >= 2 else "?"
            solution.append((step, moves.strip()))
    return solution


def extract_cross(solution: List[Tuple[str, str]]):
    return filter(solution, lambda pair: "cross" in pair[0])

def save_cross_solution():
    number_of_reconstructions = 5824 # check it out on http://www.cubesolv.es/ (visible in latest reconstruction URL)
    url_generator = "http://www.cubesolv.es/solve/{}".format
    cross_solutions = []
    wrong_urls = []
    for reconstruction_number in tqdm(range(1, number_of_reconstructions + 1)):
        url = url_generator(reconstruction_number)
        try:
            solution = extract_solution(url)
            for step in solution: 
                # solution might have multiple steps with cross inside: for example pseudo-cross -> xcross 
                # (see http://www.cubesolv.es/solve/31 or Tymon's solutions)
                if "cross" in step[0]:
                    print(step[0])
                    if len(step[1]) > 0:
                        cross_solutions.append((reconstruction_number, *step))
                    else:
                        print("Empty cross at {}".format(reconstruction_number))
                        wrong_urls.append(url + "\n")
        except IndexError:
            print("Error occurred at {}".format(reconstruction_number))
            wrong_urls.append(url + "\n")
        if reconstruction_number % 1000 == 0:
            cross_solution_df = pd.DataFrame(cross_solutions, columns=["number", "step_name", "solution"])
            cross_solution_df.to_csv("cross_solutions.csv")

            
    print("Number of not processed URLs: {}".format(len(wrong_urls)))
    print("Wrong URLs:")
    print(wrong_urls)
    cross_solution_df = pd.DataFrame(cross_solutions, columns=["number", "step_name", "solution"])
    cross_solution_df.to_csv("cross_solutions.csv")
    with open("wrong_urls.txt", "w") as f:
        f.writelines(wrong_urls)


if __name__ == "__main__":
    save_cross_solution()

    


