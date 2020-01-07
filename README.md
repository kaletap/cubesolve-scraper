Simple tool to scrape Rubik's Cube solutions from cubesolv.es and analyze them.

* **scraper.py** scrapes solutions and saves them in `cross_solutions.csv`. Also produces a files with urls that failed, `wrong_urls.txt`, for example because there was no cross step in the solution
* **analyze_sequences.py** finds most common sequences of k-moves among crosses in `cross_solutions.csv`

I used it to find what are the most common three move sequences during cross phase to optimize notation for TeamBLD.
