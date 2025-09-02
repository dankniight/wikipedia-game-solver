# Wikipedia Game Solver
The Wikipedia Game is a challenge where you start on one Wikipedia page and must reach a target page by clicking only the links within each article you visit.

This project uses a breadth-first search (BFS) algorithm to find the shortest path between two Wikipedia pages. It interacts with the Wikipedia API to retrieve page links and navigate through them.
The project is a simple proof-of-concept for my portfolio, as the 1-second crawl delay to comply with wikipedia's limits means the program can easily run for hours depending on the input.

## Example Path
**Starting Page:** Tetris  
**Target Page:** Daft Punk

```mermaid
flowchart LR
    A[Tetris] --> B[Amiga]
    B --> C["Weird Al" Yankovic]
    C --> D[Daft Punk]
    

```

## How It Works

1.  The user provides a starting Wikipedia page title and a target page title.
2.  The script normalizes these titles (e.g., replacing spaces with underscores).
3.  It uses a BFS algorithm to explore links from the starting page.
4.  For each page, it fetches all outgoing links using the Wikipedia API.
5.  It checks if any of these links are the target page.
6.  If not, it adds the new links to a queue to be explored in the next iteration (keeping track of the path taken).
7.  This process continues until the target page is found or the search space is exhausted (or a depth limit is reached).


## Usage

1.  Ensure you have Python and the `requests` library installed.
2.  Run the script: `python main.py`
3.  Enter the starting Wikipedia page title when prompted.
4.  Enter the target Wikipedia page title when prompted.
5.  The script will search for a path and display the result.

**Note:** The search can take a while, especially for distant pages, due to the intentional delays between API requests to be respectful to Wikipedia's servers.